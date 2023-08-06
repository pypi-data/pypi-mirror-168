import aws_cdk
import constructs
import well_architected_constructs

from . import well_architected_stack


class RestApiSnsLambdaEventBridgeLambda(well_architected_stack.Stack):

    def __init__(self, scope: constructs.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        event_bus = self.create_event_bus(id)
        name = 'destined'
        sns_topic = self.create_sns_topic(f'{name}SnsTopic')
        self.create_success_lambda(event_bus)
        self.create_failure_lambda(event_bus)
        self.create_sns_triggered_lambda(
            name=name,
            event_bus=event_bus,
            sns_topic=sns_topic,
        )

        well_architected_constructs.rest_api_sns.RestApiSnsConstruct(
            self, 'RestApiSns',
            error_topic=self.error_topic,
            method='GET',
            message="please $input.params().querystring.get('mode')",
            sns_topic_arn=sns_topic.topic_arn,
        )

    def create_success_lambda(self, event_bus):
        return self.create_event_driven_lambda_function(
            function_name="success",
            event_bus=event_bus,
            description='all success events are caught here and logged centrally',
            response_payload={
                "source": ["cdkpatterns.the-destined-lambda"],
                "action": ["message"]
            },
            additional_details={
                "requestContext": {
                    "condition": ["Success"]
                }
            },
        )

    def create_failure_lambda(self, event_bus):
        return self.create_event_driven_lambda_function(
            function_name="failure",
            event_bus=event_bus,
            description='all failure events are caught here and logged centrally',
            response_payload={
                "errorType": ["Error"]
            },
        )

    def create_sns_triggered_lambda(
        self, name=None, event_bus=None, sns_topic=None
    ):
        return self.create_lambda_function(
            function_name=f"{name}_lambda",
            retry_attempts=0,
            on_success=aws_cdk.aws_lambda_destinations.EventBridgeDestination(event_bus=event_bus),
            on_failure=aws_cdk.aws_lambda_destinations.EventBridgeDestination(event_bus=event_bus),
            sns_trigger_topic=sns_topic,
            duration=None,
        )

    def create_event_bus(self, name):
        return aws_cdk.aws_events.EventBus(
            self, 'EventBus',
            event_bus_name=name,
        )

    def create_event_driven_lambda_function(
        self, event_bus=None, description=None, function_name=None,
        response_payload=None, additional_details={}
    ):
        details = {
            "responsePayload": response_payload
        }
        details.update(additional_details)
        self.create_lambda_function(
            function_name=function_name,
            event_bridge_rule=aws_cdk.aws_events.Rule(
                self, f'event_bridge_rule_{function_name}',
                event_bus=event_bus,
                description=description,
                event_pattern=aws_cdk.aws_events.EventPattern(
                    detail=details,
                )
            ),
        )

    def create_lambda_function(
        self,
        duration=3,
        event_bridge_rule=None,
        function_name=None,
        on_failure=None,
        on_success=None,
        retry_attempts=2,
        sns_trigger_topic=None,
    ):
        return well_architected_constructs.lambda_function.LambdaFunctionConstruct(
            self, function_name,
            retry_attempts=retry_attempts,
            error_topic=self.error_topic,
            lambda_directory=self.lambda_directory,
            event_bridge_rule=event_bridge_rule,
            sns_trigger_topic=sns_trigger_topic,
            on_success=on_success,
            on_failure=on_failure,
            duration=duration
        ).lambda_function
