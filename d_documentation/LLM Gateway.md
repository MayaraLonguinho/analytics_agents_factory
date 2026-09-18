# LLM Gateway

## Responsibility
Fachada e roteador único de modelos de linguagem (`ModelRouter`), desacoplando provedores da lógica dos agentes. O suporte operacional ativo é exclusivo para [[OpenAI Provider]] (`gpt-4o-mini`); integrações Anthropic e Gemini declaram-se não implementadas (`NotImplementedError`).

## Path
`a_platform/j_llm_gateway/d_gateway.py`

## Inputs
[[Agents]]

## Outputs
LLMResponse padronizada

## Integrations
- [[OpenAI Provider]]

## Failure behavior
Lança exceção de provider, timeout ou `NotImplementedError` caso provedor desabilitado seja solicitado.
