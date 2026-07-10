from aws_cdk import (
    Stack,
    aws_apigatewayv2 as apigw,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    CfnOutput,
    CfnParameter,
    RemovalPolicy
)
from constructs import Construct

class ApiGatewayStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(self, "ExclusaoClientesTable",
            partition_key=dynamodb.Attribute(name="cliente_id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="request_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        lambda_function_name = CfnParameter(self, "LambdaFunctionName", type="String", default="exclusao-cliente-lambda")

        lambda_fn = _lambda.Function.from_function_name(self, "ExclusaoClienteLambda", lambda_function_name.value_as_string)

        http_api = apigw.HttpApi(
            self, "ExclusaoClienteHttpApi",
            description="API Gateway para Exclusão de Cliente com Pix",
            cors_preflight=apigw.CorsPreflightOptions(allow_origins=["*"], allow_methods=[apigw.CorsHttpMethod.ANY]),
            throttle=apigw.ThrottleSettings(rate_limit=100, burst_limit=200)
        )

        lambda_integration = apigw.HttpLambdaIntegration("LambdaIntegration", lambda_fn)

        http_api.add_routes(path="/solicitar-exclusao-cliente", methods=[apigw.HttpMethod.POST], integration=lambda_integration)
        http_api.add_routes(path="/status-exclusao/{cliente_id}", methods=[apigw.HttpMethod.GET], integration=lambda_integration)
        http_api.add_routes(path="/confirmar-pagamento", methods=[apigw.HttpMethod.POST], integration=lambda_integration)

        CfnOutput(self, "ApiUrl", value=http_api.url)
        CfnOutput(self, "ApiId", value=http_api.api_id)
        CfnOutput(self, "DynamoTableName", value=table.table_name)