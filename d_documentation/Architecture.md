# Architecture

## Responsibility
Decisão técnica de alto nível com base no Brain e DatasetProfile, definindo a stack tecnológica, estratégia de persistência e padrões de projeto.

## Path
`a_platform/g_agents/c_architecture/a_architecture_agent.py`

## Inputs
[[Brain]], [[Orchestrator]]

## Outputs
ArchitectureDecision (stack, persistência, componentes exigidos)

## Integrations
- [[Planner]]

## Failure behavior
Interrompe o pipeline impedindo a fase de planejamento caso a decisão arquitetural seja inconsistente.
