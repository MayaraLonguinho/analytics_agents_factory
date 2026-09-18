# Command Policy

## Responsibility
Política restritiva de segurança e isolamento para execução de comandos no sistema operacional. Opera em duas posições fundamentais:
1. **Planning (Preflight):** Validação estática de comandos durante a elaboração do plano pelo [[Planner]].
2. **Runtime (Enforcement):** Aplicação compulsória no momento do disparo de subprocessos pelo [[Runtime]], garantindo `shell=False`, argumentos explicitados e bloqueio de binários não autorizados.

## Path
`a_platform/k_runtime/b_command_policy/a_command_policy.py`

## Inputs
[[Planner]], [[Runtime]]

## Outputs
Decisão de conformidade (`ALLOWED` ou `DENIED`)

## Integrations
- [[Planner]]
- [[Runtime]]

## Failure behavior
Emissão de status `DENIED`, bloqueando imediatamente o planejamento da tarefa ou a execução do subprocesso em disco.
