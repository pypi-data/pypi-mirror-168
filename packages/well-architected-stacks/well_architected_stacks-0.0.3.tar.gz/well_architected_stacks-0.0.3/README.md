# Well Architected

Python Well-Architected CDK Patterns from https://cdkpatterns.com/patterns/well-architected/

# Available Stacks

- ApiLambdaRds
- ApiLambdaDynamodb
- ApiLambdaDynamodbEventBridgeLambda
- AutoscalingEcsService
- AutoscalingEcsServiceWithPlacement
- AutoscalingEcsCluster
- AlbAutoscalingEcsService
- NlbAutoscalingEcsService
- NlbFargateService
- NlbAutoscalingFargateService
- ApiLambdaEventBridgeLambda
- ApiLambdaSqsLambdaDynamodb
- ApiSnsLambdaEventBridgeLambda
- ApiSnsSqsLambda
- ApiStepFunctions
- LambdaFat
- LambdaLith
- LambdaPowerTuner
- LambdaSinglePurpose
- RestApiDynamodb
- RestApiSns
- S3SqsLambdaEcsEventBridgeLambdaDynamodb
- SagaStepFunction
- SimpleGraphqlService
- SnsLambda
- SnsLambdaSns
- SnsLambdaDynamodb
- SqsLambdaSqs
- WafApiLambdaDynamodb

# Examples

## Using a Well Architected Stack

```Python
import aws_cdk
import well_architected_stacks

app = aws_cdk.App()
well_architected_stacks.api_lambda_eventbridge_lambda.ApiLambdaDynamodbEventBridgeLambda(
    app, 'ApiLambdaDynamodbEventBridgeLambda
)
app.synth()
```
