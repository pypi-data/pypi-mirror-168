import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class SnsLambdaDynamodb(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        sns_topic=None,
        partition_key=None,
        lambda_function_name=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.dynamodb_table = well_architected_constructs.dynamodb_table.DynamodbTableConstruct(
            self, "DynamoDbTable",
            partition_key=partition_key,
            error_topic=self.error_topic,
        ).dynamodb_table

        self.lambda_function = well_architected_constructs.sns_lambda.SnsLambdaConstruct(
            self, 'SnsLambda',
            function_name=lambda_function_name,
            sns_topic=sns_topic,
            error_topic=self.error_topic,
            lambda_directory=self.lambda_directory,
            environment_variables={
                "HITS_TABLE_NAME": self.dynamodb_table.table_name
            }
        ).lambda_function

        self.dynamodb_table.grant_read_write_data(
            self.lambda_function
        )