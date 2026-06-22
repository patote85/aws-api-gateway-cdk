from aws_cdk import (
    Stack, aws_apigatewayv2 as apigw, aws_apigatewayv2_authorizers as auth, aws_lambda as _lambda
)
from constructs import Construct

class ApiGatewayStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Authorizer Lambda (deployed from other repo)
        authorizer_fn = _lambda.Function.from_function_name(self, 'AuthorizerLambda', 'exclusao-authorizer')
        
        authorizer = auth.HttpLambdaAuthorizer(
            'CustomAuthorizer',
            authorizer_fn,
            authorizer_name='CustomAuthorizer'
        )
        
        http_api = apigw.HttpApi(self, 'ExclusaoApi', authorizer=authorizer)
        # ... rotas com authorizer aplicado