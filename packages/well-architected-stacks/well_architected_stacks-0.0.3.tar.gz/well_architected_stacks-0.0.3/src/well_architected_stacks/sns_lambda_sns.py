import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class SnsLambdaSns(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_publisher_trigger=None,
        publisher_lambda_name=None,
        subscriber_lambda_name=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        topic = aws_cdk.aws_sns.Topic(
            self, 'SnsTopic',
            display_name='SnsTopic'
        )

        self.create_lambda_function(
            construct_id='SnsSubscriber',
            function_name=subscriber_lambda_name,
            sns_topic=topic,
        )

        sns_publisher = self.create_lambda_function(
            construct_id='SnsPublisher',
            function_name=publisher_lambda_name,
            sns_topic=sns_publisher_trigger,
            environment_variables={
                'TOPIC_ARN': topic.topic_arn,
            }
        )

        topic.grant_publish(sns_publisher)

    def create_lambda_function(
        self, construct_id=None, function_name=None, sns_topic=None,
        environment_variables=None,
    ):
        return well_architected_constructs.sns_lambda.SnsLambdaConstruct(
            self, construct_id,
            function_name=function_name,
            lambda_directory=self.lambda_directory,
            sns_topic=sns_topic,
            error_topic=self.error_topic,
            environment_variables=environment_variables,
        ).lambda_function