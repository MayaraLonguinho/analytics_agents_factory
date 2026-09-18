# Planner

## Papel no Golden Path
Decomposição determinística da decisão arquitetural em um plano de tarefas atômicas e ordenadas (`ProjectPlan`). O `PlannerAgent` valida formalmente:
1. Agentes permitidos contra o domínio e registrados no `AgentRegistry`;
2. Skills requeridas no catálogo `b_skills.yaml`;
3. MCPs autorizados;
4. Ausência de dependências circulares (grafo acíclico - DAG);
5. Preflight de segurança dos comandos de execução contra a `CommandPolicy`;
6. Injeção de comandos de verificação de qualidade física (`pytest`, `flake8`, `bandit`, `pip check`).

## Posição no Fluxo
← **Anterior:** [[e_architecture|Architecture]]  
→ **Próximo:** [[g_project_factory|Project Factory]]

## Entrada e Saída
- **Entrada:** `request.architecture_decision` e `request.brain_context`.
- **Saída:** `request.project_context.plan` (`ProjectPlan` estruturado com `tasks` e `run_commands`).

## Integrações e Contratos
- Componente: `a_platform/g_agents/d_planner/k_planner_agent.py`
- Contratos: `a_platform/b_contracts/f_plan.py` e `e_task.py`
- Preflight: `a_platform/k_runtime/b_command_policy/a_policy.py`

## Referência Técnica
Para detalhes da política de comandos e restrições de execução, consulte [[h_command_policy|Política de Comandos]].
