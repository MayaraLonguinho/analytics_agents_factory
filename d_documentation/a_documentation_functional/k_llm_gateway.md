# LLM Gateway

## Papel no Golden Path
Ponto focal unificado para todas as inferências com modelos de inteligência artificial. Roteia as chamadas para o provedor habilitado (OpenAI Provider com o modelo `gpt-4o-mini` por padrão), gerencia parâmetros de temperatura e contexto, e valida o preenchimento de `LLMResponse.content`.

## Posição no Fluxo
← **Anterior:** [[j_mcps|MCPs]]  
→ **Próximo:** [[l_artifact|Artifact]]

## Entrada e Saída
- **Entrada:** `prompt`, mensagens ou schemas de saída estruturada.
- **Saída:** Objeto canônico `LLMResponse` contendo o texto puro gerado (`content`), modelo utilizado e metadados.

## Integrações e Contratos
- Gateway: `a_platform/j_llm_gateway/d_gateway.py` (`LLMGateway`)
- Provedor Ativo: `a_platform/j_llm_gateway/b_providers/a_openai/a_provider.py` (`OpenAIProvider`)

## Referência Técnica
Para detalhes de roteamento, providers e chaves de API, consulte [[g_llm_provider|Provedor de LLM]].
