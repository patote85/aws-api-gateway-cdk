# AWS API Gateway CDK

Repositório de Infrastructure as Code para API Gateway HTTP.

## Integração com Lambda (outro repositório)

1. Deploy da Lambda primeiro (repo: aws-lambda-api-gateway-python)
2. Passe o nome da função Lambda como parâmetro

## Deploy
```bash
cdk deploy --parameters LambdaFunctionName=exclusao-cliente-lambda
```

## Rotas
- POST /solicitar-exclusao-cliente
- GET /status-exclusao/{cliente_id}
- POST /confirmar-pagamento