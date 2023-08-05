import constructs
import well_architected_constructs

from . import well_architected_stack
from . import api_lambda_dynamodb


class WafApiLambdaDynamodb(api_lambda_dynamodb.ApiLambdaDynamodbStack):

    def __init__(
        self, scope: constructs.Construct, id: str,
        partition_key='path',
        sort_key=None,
        **kwargs
    ):
        super().__init__(
            scope, id,
            partition_key=partition_key,
            **kwargs
        )
        self.name = self.camel_to_snake(id)
        self.rest_api = self.api_lambda_dynamodb.create_rest_api_lambda()
        self.web_application_firewall = well_architected_constructs.web_application_firewall.WebApplicationFirewall(
            self, 'WebApplicationFirewall',
            error_topic=self.error_topic,
            target_arn= f"arn:aws:apigateway:region::/restapis/{self.rest_api.api_id}/stages/{self.rest_api.api.deployment_stage.stage_name}",
        )

    @staticmethod
    def camel_to_snake(text):
        return ''.join([
            '_'+character.lower()
            if character.isupper()
            else character
            for character in text
        ]).lstrip('_')