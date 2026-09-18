# Repair Loop

## Responsibility
Mecanismo de autorrecuperação reativa. Avalia diagnósticos de falhas de execução ou sintaxe e reengaja os agentes respectivos para correção e nova materialização (até o limite de 3 tentativas).

## Path
`a_platform/o_orchestration/c_repair_loop.py`

## Inputs
[[Validation]], [[Orchestrator]]

## Outputs
Nova versão de artefatos corrigidos submetidos a reexecução

## Integrations
- [[Agents]]
- [[Materializer]]
- [[Runtime]]
- [[Validation]]

## Failure behavior
Ao esgotar `max_repair_attempts` (3), declara falha irrecuperável e transiciona o projeto para `FAILED`.
