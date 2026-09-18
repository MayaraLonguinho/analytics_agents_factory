# LLM Gateway e Provedor OpenAI

O subsistema de LLM (`a_platform/j_llm_gateway`) encapsula e isola todas as interações com modelos de inteligência artificial na Analytics Agents Factory. Nenhum componente ou agente da plataforma realiza chamadas diretas a bibliotecas de LLM sem a intermediação do Gateway.

## Arquitetura do Gateway

O Gateway está estruturado em:

- **a_gateway/a_gateway.py (`LLMGateway`)**: Ponto central de entrada para requisições de geração de texto, chat completion e structured output.
- **c_router/a_router.py (`ModelRouter`)**: Roteia solicitações para o provedor e modelo adequados com base na configuração do sistema.
- **b_providers/**: Adaptadores para provedores de inteligência artificial.

## Provedor Operacional: OpenAI Provider

O provedor padrão e homologado do AAF é implementado em:
`a_platform/j_llm_gateway/b_providers/a_openai/a_provider.py`

### Características Técnicas

- **Modelo Canônico:** `gpt-4o-mini`, configurado como modelo de referência para velocidade, custo e capacidade analítica estruturada.
- **SDK:** Utiliza o SDK oficial da OpenAI (`openai` client) com autenticação via variável de ambiente `OPENAI_API_KEY`.
- **Mapeamento de Tipos:** Converte respostas nativas de ChatCompletion em instâncias tipadas de `LLMResponse`.
- **Tratamento de Exceções:** Captura erros de rede, autenticação, rate limiting e quotas, encapsulando-os em exceções tipadas de plataforma (`LLMException`).

## Tratamento de Falhas

Se a chave `OPENAI_API_KEY` estiver ausente ou inválida, o Gateway falha de forma explícita e antecipada, impedindo que tarefas avancem com dados incompletos ou mocks não autorizados.
