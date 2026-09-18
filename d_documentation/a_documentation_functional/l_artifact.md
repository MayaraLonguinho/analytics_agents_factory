# Artifact

## Papel no Golden Path
Unidade atômica tipada de código ou recurso produzida pela fábrica. Representa cada arquivo de software gerado (código-fonte, script SQL, teste automatizado, arquivo de configuração ou documentação) antes da gravação física em disco.

## Posição no Fluxo
← **Anterior:** [[k_llm_gateway|LLM Gateway]]  
→ **Próximo:** [[m_materializer|Materializer]]

## Entrada e Saída
- **Entrada:** Código gerado por agentes, skills ou templates.
- **Saída:** Instâncias da classe Pydantic `Artifact` com atributos canônicos: `identity`, `name`, `path`, `type`, `content`, `metadata` e `producer`.

## Integrações e Contratos
- Contrato: `a_platform/b_contracts/g_artifact.py`
- Campo Canônico de Localização: `Artifact.path`

## Referência Técnica
Para as regras de tipagem e integridade estrutural, consulte [[a_architecture|Arquitetura Geral]].
