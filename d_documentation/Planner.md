# Planner

## Responsibility
Single Source of Truth do plano atômico de execução (`ProjectPlan`). Realiza validações estritas pré-execução de: domínio, autorização de agentes no AgentRegistry, skills declaradas no catálogo `b_skills.yaml`, MCPs permitidos, stack arquitetural, comandos permitidos via preflight de [[Command Policy]] e requisitos de evidência tipada.

## Path
`a_platform/g_agents/d_planner/k_planner_agent.py`

## Inputs
[[Architecture]], [[Orchestrator]]

## Outputs
ProjectPlan (DAG de Tasks com `assigned_agent`, `skills`, `mcps` e `run_commands`)

## Integrations
- [[Command Policy]]
- [[Project Factory]]

## Failure behavior
Interrupção da orquestração com erro tipado em caso de agente não autorizado, skill inexistente, comando inválido ou inconsistência de domínio.
