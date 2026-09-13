# Operação da Plataforma

A Analytics Agents Factory (AAF) opera primariamente orientada a eventos iniciados via CLI. O fluxo garante o gerenciamento de estados no ciclo de vida de um projeto gerado.

## Como iniciar o AAF
A AAF expõe sua CLI em `a_platform/b_interfaces/b_cli/c_commands.py`.

Iniciando um novo projeto através de um prompt de requisição:
```bash
python -m a_platform.b_interfaces.b_cli.c_commands start --prompt "Crie um pipeline ETL para ler os dados de vendas, deduplicar as linhas e salvar no SQLite" --dataset "./d_input/vendas.csv"
```

## Como utilizar a CLI
A CLI oferece outros submódulos essenciais:
- `status`: Checar o status da máquina de estado de um projeto rodando ou paralisado (aguardando input).
  ```bash
  python -m a_platform.b_interfaces.b_cli.c_commands status --id "proj-xyz"
  ```
- `result`: Recuperar os dados e relatório do projeto gerado.
- `brain`: Acessar metadados, regras e estado do Brain para telemetria.
- `mcp`: Acionar *tools* de forma desacoplada para depuração manual de permissões (ex: execução de Docker ou Queries).

## Fluxo Operacional e Estados (State Manager)
O arquivo `c_state.py` governa transições estritas:
1. `INIT` → Criação do `AAFSession` e identificador.
2. `IN_PROGRESS` → Executando fases de orquestração.
3. `NEEDS_INPUT` → Pipeline pausa solicitando esclarecimento (normalmente na fase de Discovery).
4. `FAILED` → O ciclo de execução falhou fatalmente além das tentativas de `Repair`.
5. `READY` → O projeto atingiu a maturidade em todas as checagens e Gates.

Cada fase de execução transaciona nos seguintes passos do `a_orchestrator`:
Discovery → Profiling → Brain → Architecture → Planner → Factory → Materialization → Execution → Validation → Quality → Certification.

## Comportamento Esperado & Erros
- A plataforma não silencia erros. Se um MCP falha em criar o arquivo (ex: path crossing the sandbox), um `ExecutionError` ou notificação equivalente preenche os *diagnostics*.
- Se as chaves de API estiverem ausentes, o Gateway atirará falha ao invés de prosseguir silenciosamente.
- Se a Certificação falhar ao verificar testes de unidade (`tests_ok = False`), a fábrica reporta FALHA no Certification Report.
- A orquestração repetirá a execução (Repair Loop) até o `max_repair_attempts` para corrigir anomalias de sintaxe e testes antes de admitir a falha ao usuário.
