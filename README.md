> **Arquivado (ADR-001).** A stack canônica vive em [`patote85/aws-lambda-api-gateway-python`](https://github.com/patote85/aws-lambda-api-gateway-python) (`cdk/`). Este repositório permanece só como referência histórica — não use para deploy novo.

# AWS API Gateway CDK

## Visão Geral
Infraestrutura como Código para API Gateway HTTP integrada com a Lambda de Exclusão de Cliente.

**Este projeto segue os Karpathy Claude Guidelines.**

## Melhorias Implementadas
- Throttling configurado (rate 100, burst 200)
- Parâmetro para nome da Lambda
- Estrutura preparada para Authorizer

**Code Review:** Aprovado.

**Merge realizado para main.**
