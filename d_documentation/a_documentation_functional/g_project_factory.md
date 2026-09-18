# Project Factory

## Papel no Golden Path
Orquestrador de geração serial de código. Percorre as tarefas ordenadas topologicamente no `ProjectPlan`, despacha cada uma para a instância do agente responsável obtida na `AgentFactory`, e coleta a lista completa de artefatos gerados (`Artifact[]`). Realiza checagem *fail-fast* garantindo que todos os `expected_artifacts` foram produzidos.

## Posição no Fluxo
← **Anterior:** [[f_planner|Planner]]  
→ **Próximo:** [[h_agents|Agents]]

## Entrada e Saída
- **Entrada:** `request.project_context.plan` (`ProjectPlan`) e `AgentFactory`.
- **Saída:** `request.project_context.generated_artifacts` (`List[Artifact]`).

## Integrações e Contratos
- Componente: `a_platform/h_factory/a_project_factory.py`
- Fábrica de agentes: `a_platform/g_agents/n_factory/a_agent_factory.py`

## Referência Técnica
Para detalhes do ciclo de vida dos agentes e despacho de tarefas, consulte [[f_agents|Sistema de Agentes]].
