# Discovery

## Responsibility
Análise e levantamento inicial de requisitos técnicos e objetivos de negócio. Pausa de forma idempotente via `NEEDS_INPUT` e `StateManager` se dados essenciais estiverem ausentes, sem realizar perguntas redundantes sobre características físicas de datasets fornecidos.

## Path
`a_platform/g_agents/b_discovery/a_discovery_agent.py`

## Inputs
[[Orchestrator]]

## Outputs
Project Context / Discovery Dossier (`discovery_data`)

## Integrations
- [[Dataset Profiling]]

## Failure behavior
Emite `missing_info_question`, salva o estado em disco como `PAUSED` e aguarda retorno do usuário via `--answer` (ou falha caso exceda o limite de 5 perguntas).
