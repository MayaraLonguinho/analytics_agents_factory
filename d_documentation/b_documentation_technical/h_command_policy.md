# Command Policy

A `CommandPolicy` (`a_platform/k_runtime/b_command_policy/a_policy.py`) é o mecanismo de segurança e isolamento responsável por auditar e restringir a execução de comandos no sistema operacional dentro da Analytics Agents Factory.

## Dupla Posição de Atuação

A política atua em dois momentos cruciais do pipeline:

1. **Planning (Preflight):**
   - Durante a elaboração do plano pelo `PlannerAgent`.
   - O `Planner` submete todos os `run_commands` propostos para a `CommandPolicy`.
   - Comandos com sintaxe insegura, binários não autorizados ou operadores de shell proibidos são imediatamente rejeitados com status `DENIED`, abortando ou forçando a reformulação da tarefa antes da execução.

2. **Runtime (Enforcement):**
   - No momento do disparo de subprocessos pelo `RuntimeEngine` (`a_platform/k_runtime/a_execution/a_runtime.py`).
   - Aplicação compulsória de execução sem shell (`shell=False`), argumentos fornecidos estritamente como lista (`list[str]`) e validação do caminho do binário.

## Regras de Segurança

- **Binários Permitidos:** Apenas binários explicitamente listados na política são autorizados (ex: `python`, `pytest`, `pip`).
- **Proibição de Shell:** Proibição absoluta de execução de comandos através de interpretadores intermediários (`/bin/sh`, `/bin/bash`, `cmd.exe`) ou concatenação com operadores (`&&`, `||`, `;`, `|`).
- **Isolamento de Diretório:** A execução é restrita ao diretório do projeto gerado em `e_generated_projects/<project_id>/`.

## Comportamento em Caso de Violação

Tentativas de execução de comandos não aprovados resultam em exceção imediata (`CommandPolicyViolationError`), interrupção da tarefa e registro detalhado da violação nos logs de auditoria.
