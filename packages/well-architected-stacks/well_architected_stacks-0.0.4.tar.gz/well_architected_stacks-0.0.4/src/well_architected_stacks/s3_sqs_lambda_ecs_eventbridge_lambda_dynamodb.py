import json
import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class S3SqsLambdaEcsEventBridgeLambdaDynamodb(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        containers_directory=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.dynamodb_table = self.create_dynamodb_table()
        self.sqs_queue = self.create_sqs_queue()
        self.vpc = self.create_vpc()
        self.ecs_cluster = self.create_ecs_cluster(self.vpc)
        self.ecs_task_definition = self.create_ecs_task_definition(
            self.event_bridge_iam_policy()
        )

        self.s3_bucket = self.create_s3_bucket_with_sqs_destination(
            sqs_queue=self.sqs_queue,
            ecs_task_role=self.ecs_task_definition.task_role,
        )

        self.extractor = self.create_sqs_subscriber_lambda_function(
            ecs_task_definition=self.ecs_task_definition,
            sqs_queue=self.sqs_queue,
            ecs_cluster_name=self.ecs_cluster.cluster_name,
            vpc=self.vpc,
            image_name=f'{containers_directory}/s3DataExtractionTask',
            s3_bucket_name=self.s3_bucket.bucket_name,
            s3_object_key=''
        )
        self.grant_ecs_task_permissions(
            ecs_task_definition=self.ecs_task_definition,
            lambda_function=self.extractor,
        )

        self.transformer = self.create_lambda_function(
            function_name='transformer',
            event_bridge_rule_description='Data extracted from S3, Needs transformation',
            event_bridge_detail_type='s3RecordExtraction',
            event_bridge_detail_status="extracted",
        )

        self.loader = self.create_lambda_function(
            function_name="loader",
            event_bridge_rule_description='Load Transformed Data to DynamoDB',
            event_bridge_detail_type='transform',
            event_bridge_detail_status="transformed",
            environment_variables={
                "DYNAMODB_TABLE_NAME": self.dynamodb_table.table_name
            },
        )
        self.dynamodb_table.grant_read_write_data(self.loader)

        self.add_policies_to_lambda_functions(
            self.extractor,
            self.transformer,
            self.loader,
            policy=self.event_bridge_iam_policy()
        )

        self.create_lambda_function(
            function_name="observer",
            event_bridge_rule_description='observe and log all events'
        )

    def create_vpc(self):
        return aws_cdk.aws_ec2.Vpc(self, "Vpc", max_azs=2)

    def create_ecs_cluster(self, vpc):
        return aws_cdk.aws_ecs.Cluster(self, 'EcsCluster', vpc=vpc)

    def create_ecs_task_definition(self, iam_policy):
        task_definition = aws_cdk.aws_ecs.TaskDefinition(
            self, 'FargateTaskDefinition',
            memory_mib="512",
            cpu="256",
            compatibility=aws_cdk.aws_ecs.Compatibility.FARGATE
        )
        task_definition.add_to_task_role_policy(iam_policy)
        return task_definition

    def create_ecs_container(self, ecs_task_definition=None, s3_bucket_name=None, s3_object_key=None, image_name=None):
        return ecs_task_definition.add_container(
            'AppContainer',
            image=aws_cdk.aws_ecs.ContainerImage.from_asset(image_name),
            logging=self.get_logging_configuration(),
            environment={
                'S3_BUCKET_NAME': s3_bucket_name,
                'S3_OBJECT_KEY': s3_object_key,
            }
        ).container_name

    def create_event_bridge_rule(
        self, name=None, description=None, detail_type=None, status=None,
    ):
        return aws_cdk.aws_events.Rule(
            self, f'{name}Rule',
            description=description,
            event_pattern=aws_cdk.aws_events.EventPattern(
                source=['cdkpatterns.the-eventbridge-etl'],
                detail_type=[detail_type] if detail_type else None,
                detail={"status": [status]} if status else None
            )
        )

    def create_lambda_function(
        self,
        function_name=None,
        concurrent_executions=2,
        duration=3,
        environment_variables=None,
        event_bridge_rule_description=None,
        event_bridge_detail_type=None,
        event_bridge_detail_status=None,
        sqs_trigger_queue=None,
    ):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, function_name,
            function_name=function_name,
            concurrent_executions=concurrent_executions,
            duration=duration,
            environment_variables=environment_variables,
            error_topic=self.error_topic,
            event_bridge_rule=self.create_event_bridge_rule(
                name=function_name,
                description=event_bridge_rule_description,
                detail_type=event_bridge_detail_type,
                status=event_bridge_detail_status,
            ),
            lambda_directory=self.lambda_directory,
            sqs_trigger_queue=sqs_trigger_queue,
        ).lambda_function

    def create_sqs_subscriber_lambda_function(
        self, ecs_task_definition=None,
        sqs_queue=None, s3_bucket_name=None, s3_object_key=None,
        image_name=None, ecs_cluster_name=None, vpc=None,
    ):
        return self.create_lambda_function(
            function_name='extractor',
            sqs_trigger_queue=sqs_queue,
            environment_variables={
                "CLUSTER_NAME": ecs_cluster_name,
                "SUBNETS": self.get_subnet_ids(vpc),
                "TASK_DEFINITION": ecs_task_definition.task_definition_arn,
                "CONTAINER_NAME": self.create_ecs_container(
                    ecs_task_definition=ecs_task_definition,
                    image_name=image_name,
                    s3_bucket_name=s3_bucket_name,
                    s3_object_key=s3_object_key,
                )
            },
        )

    def create_dynamodb_table(self):
        return well_architected_constructs.dynamodb_table.DynamodbTableConstruct(
            self, 'TransformedData',
            error_topic=self.error_topic,
            partition_key="id",
        ).dynamodb_table

    def create_sqs_queue(self):
        return aws_cdk.aws_sqs.Queue(
            self,
            'newObjectInLandingBucketEventQueue',
            visibility_timeout=aws_cdk.Duration.seconds(300)
        )

    def create_s3_bucket_with_sqs_destination(
        self, sqs_queue:aws_cdk.aws_sqs.Queue=None,
        ecs_task_role:aws_cdk.aws_iam.Role=None,
    ):
        s3_bucket = aws_cdk.aws_s3.Bucket(self, "LandingBucket")
        s3_bucket.add_event_notification(
            aws_cdk.aws_s3.EventType.OBJECT_CREATED,
            aws_cdk.aws_s3_notifications.SqsDestination(sqs_queue)
        )
        s3_bucket.grant_read(ecs_task_role)
        return s3_bucket

    @staticmethod
    def create_iam_policy(resources=None, actions=None):
        return aws_cdk.aws_iam.PolicyStatement(
            effect=aws_cdk.aws_iam.Effect.ALLOW,
            resources=resources if resources else ["*"],
            actions=actions
        )

    def event_bridge_iam_policy(self):
        return self.create_iam_policy(actions=['events:PutEvents'])

    def add_policies_to_lambda_functions(self, *lambda_functions, policy=None):
        for lambda_function in lambda_functions:
            lambda_function.add_to_role_policy(policy)

    def grant_ecs_task_permissions(self, ecs_task_definition=None, lambda_function=None):
        for policy in (
            self.create_iam_policy(
                resources=[ecs_task_definition.task_definition_arn],
                actions=['ecs:RunTask']
            ),
            self.create_iam_policy(
                resources=[
                    ecs_task_definition.obtain_execution_role().role_arn,
                    ecs_task_definition.task_role.role_arn
                ],
                actions=['iam:PassRole']
            )
        ):
            self.add_policies_to_lambda_functions(lambda_function, policy=policy)

    @staticmethod
    def get_subnet_ids(vpc):
        return json.dumps([subnet.subnet_id for subnet in vpc.private_subnets])

    @staticmethod
    def get_logging_configuration():
        return aws_cdk.aws_ecs.AwsLogDriver(
            stream_prefix='TheEventBridgeETL',
            log_retention=aws_cdk.aws_logs.RetentionDays.ONE_WEEK
        )