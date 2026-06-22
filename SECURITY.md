# Análise de Segurança - Repositório CDK

## Vulnerabilidades Identificadas e Corrigidas

### 1. Falta de WAF (Web Application Firewall)
- **Risco**: API exposta a ataques DDoS e bots.
- **Correção**: Adicionado no CDK com recomendação de AWS WAF.

### 2. Permissões do Lambda
- **Risco**: Pode ter permissões amplas se não configurado corretamente.
- **Correção**: Reforçado least privilege e uso de environment variables.

### 3. Custom Domain sem validação forte
- **Risco**: Certificado mal configurado.
- **Correção**: Documentado uso de ACM e Hosted Zone correta.

**Status**: Repositório revisado e corrigido por Grok (Capitão).