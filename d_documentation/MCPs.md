# MCPs

## Responsibility
Protocolos de interação segura com o ambiente local sob sandbox rigoroso: Filesystem (`is_safe_path`), Database (`is_safe_query`) e Docker (whitelist de subcomandos).

## Path
`a_platform/f_mcps/`

## Inputs
[[Agents]]

## Outputs
MCP Tool Execution Result

## Integrations
- [[Agents]]
- [[Materializer]]

## Failure behavior
Bloqueia acessos não autorizados fora da pasta segura de projetos e levanta erro de permissão.
