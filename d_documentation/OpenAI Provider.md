# OpenAI Provider

## Responsibility
Provedor operacional homologado no AAF, executando chamadas nativas autenticadas via SDK oficial contra o modelo canônico `gpt-4o-mini`.

## Path
`a_platform/j_llm_gateway/b_providers/a_openai/a_provider.py`

## Inputs
[[LLM Gateway]]

## Outputs
OpenAI ChatCompletion mapeado para LLMResponse

## Integrations
- [[LLM Gateway]]

## Failure behavior
Lança erro de autenticação, timeout ou indisponibilidade de API.
