# Project Factory

## Responsibility
Orquestração da fábrica de geração. Instancia agentes especializados via `AgentFactory` para executar as tarefas do plano e compilar o resultado em objetos lógicos tipados.

## Path
`a_platform/h_factory/a_project_factory.py`

## Inputs
[[Planner]], [[Orchestrator]]

## Outputs
Coleção de objetos lógicos tipados (`List[Artifact]`)

## Integrations
- [[Agents]]

## Failure behavior
Interrupção da fabricação em caso de erro na execução das tarefas pelos agentes.
