# Runtime

## Responsibility
Pipeline executivo seguro e controlado para disparo de subprocessos (`shell=False`, timeouts explícitos, diretório de trabalho confinado). Aplica a política de comandos em tempo de execução e produz evidências tipadas.

## Path
`a_platform/k_runtime/a_execution/a_runtime_engine.py`

## Inputs
[[Generated Projects]], [[Orchestrator]]

## Outputs
ExecutionResult compilado com lista tipada de `CommandExecutionResult`

## Integrations
- [[Command Policy]]
- [[Validation]]

## Failure behavior
Registra `FAILED`, `DENIED` ou `TIMEOUT` no resultado de execução repassado ao Validation Gate.
