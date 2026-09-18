# Runtime e Gerenciamento de Estado

Na Analytics Agents Factory, o conceito de "runtime" abrange duas responsabilidades arquiteturais completamente distintas e isoladas:

1. **Execution Runtime (`a_platform/k_runtime/`):** O ambiente de execução segura de subprocessos para os projetos analíticos gerados.
2. **Session Runtime State (`h_runtime/state/`):** A persistência do estado operacional e pause/resume das sessões do próprio AAF.

---

## 1. Execution Runtime (`a_platform/k_runtime/`)

O `k_runtime` é o motor de execução que gerencia o ciclo de vida físico dos projetos gerados dentro de `e_generated_projects/<project_id>/`.

### Componentes Internos

- **a_execution/a_runtime.py (`RuntimeEngine`):**
  - Intercepta as tarefas da fase de materialização e executa os `run_commands` planejados.
  - Utiliza `subprocess.Popen` com `shell=False` estrito e argumentos em lista.
  - Captura integralmente `stdout`, `stderr`, código de retorno e tempo de execução.
  - Retorna um `ExecutionResult` tipado com o status da execução (`SUCCESS`, `FAILED`).
- **b_command_policy/a_policy.py (`CommandPolicy`):**
  - Validador compulsório que garante que apenas comandos homologados e seguros sejam disparados.
- **c_artifacts/:**
  - Mecanismos de rastreamento físico dos arquivos e saídas geradas durante a execução.
- **d_health/:**
  - Verificação prévia e posterior de integridade do ambiente e containers de teste.

---

## 2. Session Runtime State (`h_runtime/state/`)

O diretório `h_runtime/state/` armazena os arquivos de estado persistente (`<project_id>.json`) que mantêm o ciclo de vida das sessões interativas da fábrica.

### Funcionamento do State Manager

- Gerenciado por `a_platform/b_contracts/j_state_manager.py` (`StateManager`).
- Permite que a fábrica pause sua execução (por exemplo, na fase de `Discovery` quando faltam requisitos essenciais) e salve o estado como `NEEDS_INPUT`.
- Permite a retomada idempotente da execução (`aaf start --project-id ... --answer ...`) restaurando o contexto sem reiniciar o fluxo do zero.
- Transições de estado suportadas: `INIT` → `IN_PROGRESS` → `NEEDS_INPUT` → `READY` / `FAILED`.
