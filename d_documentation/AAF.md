# AAF

## Responsibility
Plataforma central Analytics Agents Factory. Ponto focal que expõe comandos operacionais e orquestra o ciclo de vida analítico.

## Path
`f_cli/a_main.py` | `a_platform/b_contracts/z_interfaces/a_ide_adapter.py`

## Inputs
IDE Chat / CLI (`aaf start`)

## Outputs
Projetos Analíticos Materializados e Certificados

## Integrations
- [[Orchestrator]]

## Failure behavior
Interrupção do pipeline e emissão de diagnóstico tipado (`FAILED`).
