import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class SnsLambda(well_architected_stack.Stack):

    def __init__(
        self, scope: constructs.Construct,
        id: str,
        sns_topic: aws_cdk.aws_sns.ITopic=None,
        lambda_function_name=None,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        well_architected_constructs.sns_lambda.SnsLambdaConstruct(
            self, "SnsLambda",
            function_name=lambda_function_name,
            lambda_directory=self.lambda_directory,
            sns_topic=sns_topic,
            error_topic=self.error_topic,
        )