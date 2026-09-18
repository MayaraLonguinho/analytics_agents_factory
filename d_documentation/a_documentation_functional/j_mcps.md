# MCPs (Model Context Protocol)

## Papel no Golden Path
Camada de ferramentas e protocolos padronizados de interação com o ambiente físico. Fornece aos agentes capacidades controladas de manipulação de arquivos no disco (`filesystem_mcp`), execução de comandos e consultas a banco de dados (`database_mcp`).

## Posição no Fluxo
← **Anterior:** [[i_skills|Skills]]  
→ **Próximo:** [[k_llm_gateway|LLM Gateway]]

## Entrada e Saída
- **Entrada:** Nome do MCP e parâmetros da operação (`payload`).
- **Saída:** Dicionário padronizado com status (`ok`, `PASSED` ou `FAILED`) e dados da operação física realizada.

## Integrações e Contratos
- Executor: `a_platform/f_mcps/d_registry/b_executor.py` (`MCPExecutor`)
- Registro: `a_platform/f_mcps/d_registry/a_registry.py` (`MCPRegistry`)

## Referência Técnica
Para as implementações específicas de filesystem, banco de dados e Docker, consulte [[e_mcps|Integrações MCP]].
