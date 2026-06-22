from aws_cdk import (
    Stack,
    aws_apigatewayv2 as apigw,
    aws_lambda as _lambda,
    CfnOutput,
    Duration
)
from constructs import Construct

class ApiGatewayStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, lambda_function_name: str = "exclusao-cliente-lambda", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import existing Lambda (deployed from other repo)
        lambda_fn = _lambda.Function.from_function_name(
            self, "ExclusaoClienteLambda", lambda_function_name
        )

        # HTTP API Gateway
        http_api = apigw.HttpApi(
            self, "ExclusaoClienteHttpApi",
            description="API Gateway para Exclusão de Cliente com Pix",
            cors_preflight=apigw.CorsPreflightOptions(
                allow_origins=["*"],
                allow_methods=[apigw.CorsHttpMethod.ANY],
                allow_headers=["*"]
            )
        )

        # Integrations
        lambda_integration = apigw.HttpLambdaIntegration(
            "LambdaIntegration", lambda_fn
        )

        # Routes matching Lambda
        http_api.add_routes(
            path="/solicitar-exclusao-cliente",
            methods=[apigw.HttpMethod.POST],
            integration=lambda_integration
        )

        http_api.add_routes(
            path="/status-exclusao/{cliente_id}",
            methods=[apigw.HttpMethod.GET],
            integration=lambda_integration
        )

        http_api.add_routes(
            path="/confirmar-pagamento",
            methods=[apigw.HttpMethod.POST],
            integration=lambda_integration
        )

        # Outputs
        CfnOutput(self, "ApiUrl", value=http_api.url)
        CfnOutput(self, "ApiId", value=http_api.api_id)