# Runtime

A camada `j_runtime` foi consolidada para gerenciar rigorosamente o ciclo real de vida (execução em disco) do projeto *materializado*. Diferente das iterações legadas do despachante anterior (abandonado na raiz de `d_agents/m_execution`), este runtime encapsulado é executável.

## Execution
- **a_execution/c_runtime.py**: O cérebro local que intercepta as tarefas geradas pela fábrica na fase de materialização. Ele se apropria dos caminhos compilados via MCP e tenta disparar testes ou *setup steps* contidos no `run_commands` ditados pelo Planner.

## State
- **b_state**: A ponte persistente (localizada em disco em arquivos `.json` via `StateManager` em `d_session/c_state.py` que reflete na subpasta `/state`) onde transições críticas são acompanhadas, controlando pausas manuais e retomas (Resume Operations).

## Artifacts e Health
- **c_artifacts**: Diretivas de tracking empírico do que foi gravado fisicamente.
- **d_health**: Verifica integridade antes da entrega final (saúde de containers simulados e scripts de integridade subjacentes).

## O Ciclo de Execução no Orchestrator
Quando a máquina de estado entra no passo `ProjectPhase.EXECUTION`:
1. O runtime avalia os `run_commands` do pacote final montado pela *Project Factory*.
2. Usa invocações seguras em sandbox.
3. Captura `stdout` e `stderr`.
4. Devolve o diagnóstico formal: um `ExecutionResult` com atributo estrito de *status*.
