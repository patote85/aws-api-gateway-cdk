from aws_cdk import (
    Stack, aws_apigatewayv2 as apigw, aws_lambda as _lambda, aws_certificatemanager as acm,
    aws_route53 as route53, aws_route53_targets as targets, Duration, CfnOutput
)
from constructs import Construct

class ApiGatewayStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, lambda_function_name: str = 'exclusao-cliente-lambda', domain_name: str = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        lambda_fn = _lambda.Function.from_function_name(self, 'Lambda', lambda_function_name)
        
        http_api = apigw.HttpApi(self, 'ExclusaoApi',
            cors_preflight=apigw.CorsPreflightOptions(allow_origins=['*'], allow_methods=[apigw.CorsHttpMethod.ANY]),
            throttling=apigw.ThrottlingConfig(max_burst=100, max_rate=50)  # Throttling configurado
        )
        
        # Custom Domain (se informado)
        if domain_name:
            hosted_zone = route53.HostedZone.from_lookup(self, 'Zone', domain_name=domain_name)
            cert = acm.Certificate.from_certificate_arn(self, 'Cert', 'arn:...')  # Substitua pelo ARN
            http_api.add_domain_name('CustomDomain',
                domain_name=domain_name,
                certificate=cert
            )
            route53.ARecord(self, 'AliasRecord',
                zone=hosted_zone,
                target=route53.RecordTarget.from_alias(targets.ApiGatewayv2Domain(http_api))
            )
        
        # Routes...
        http_api.add_routes(path='/solicitar-exclusao-cliente', methods=[apigw.HttpMethod.POST], integration=apigw.HttpLambdaIntegration('Int', lambda_fn))
        # ... outras rotas
        
        CfnOutput(self, 'ApiUrl', value=http_api.url)
