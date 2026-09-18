# Operação da Plataforma

A Analytics Agents Factory (AAF) opera primariamente orientada a eventos iniciados via CLI (`f_cli/a_main.py` ou comando `aaf`) ou via adaptador de sessão (`IDEAdapter`). O fluxo garante o gerenciamento de estados no ciclo de vida de um projeto gerado.

## Separação de Papéis: IDE Chat vs Agents Nativos do AAF

- **IDE Chat:** Camada de interface e transporte de mensagens entre o usuário e a plataforma. O comando `aaf start` dispara o pipeline nativo e **não** constitui permissão para o agente da IDE gerar arquivos de projeto manualmente ou alterar o código da fábrica.
- **Agents Nativos:** Todos os passos da geração (Discovery, Arquitetura, Planejamento, Fabricação, Materialização, Execução, Validação, Qualidade, Certificação) são conduzidos exclusivamente pelos agentes internos sob o `MasterOrchestrator`.

## Como Iniciar o AAF

O ponto de entrada CLI suportado é `f_cli/a_main.py` (ou comando `aaf`):

Iniciando um novo projeto com prompt e dataset:
```bash
python f_cli/a_main.py start --project-id "vendas_analytics" --prompt "Crie um pipeline ETL para ler os dados de vendas, deduplicar as linhas e salvar no SQLite" --dataset "./b_input/c_dados_vendas.csv"
```

### Ciclo de Pause e Resume (Discovery)

Quando o `DiscoveryAgent` identifica que faltam requisitos essenciais que não podem ser inferidos das convenções do AAF, a sessão é pausada no estado `NEEDS_INPUT`, persistindo a pergunta e o estado em disco via `StateManager` (`a_platform/b_contracts/j_state_manager.py`).

Para responder e retomar na **mesma sessão**:
```bash
python f_cli/a_main.py start --project-id "vendas_analytics" --answer "Utilize formato SQLite com tabela de vendas normalizada"
```

## Comandos da CLI

A CLI oferece comandos para acompanhamento do ciclo de vida:

- `status`: Checar o status da máquina de estado de um projeto rodando ou pausado.
  ```bash
  python f_cli/a_main.py status vendas_analytics
  ```
- `result`: Recuperar os dados de materialização e relatório de certificação emitido.
  ```bash
  python f_cli/a_main.py result vendas_analytics
  ```
- `brain`: Acessar metadados, regras e decisões consolidadas no Brain.
  ```bash
  python f_cli/a_main.py brain
  ```
- `mcp`: Listar as ferramentas e protocolos MCP registrados.
  ```bash
  python f_cli/a_main.py mcp
  ```

## Separação Arquitetural de Runtimes

É crucial distinguir os dois conceitos de runtime na plataforma:

1. **`a_platform/k_runtime/` (Execution Runtime):**
   - Responsável por executar os comandos reais dos projetos gerados (`run_commands`).
   - Opera sob subprocessos com `shell=False`, validação compulsória de comandos via `CommandPolicy`, captura de `stdout`/`stderr` e testes de saúde.
2. **`h_runtime/state/` (Session Runtime State):**
   - Responsável por persistir o estado operacional das sessões do próprio AAF em arquivos JSON (`<project_id>.json`).
   - Gerenciado pelo `StateManager` para permitir operações de pause/resume durante a fase de Discovery.

## Fluxo Operacional e Estados (State Manager)

O `StateManager` (`a_platform/b_contracts/j_state_manager.py`) governa as transições persistidas em `h_runtime/state/<project_id>.json`:

1. `INIT` → Criação da sessão e identificador.
2. `IN_PROGRESS` → Executando fases de orquestração serial.
3. `NEEDS_INPUT` (`PAUSED`) → Pipeline pausa solicitando esclarecimento na fase de Discovery.
4. `FAILED` → O ciclo de execução falhou fatalmente além das tentativas do `RepairLoop`.
5. `READY` → O projeto obteve aprovação unânime em todos os gates (`PROJECT READY = YES`).

## Comportamento Esperado & Tratamento de Erros

- A plataforma não silencia erros. Se um MCP falha em criar o arquivo (ex: tentativa de escrita fora de `e_generated_projects/`), o acesso é bloqueado e a exceção é registrada nos diagnósticos.
- Se as chaves de API estiverem ausentes, o Gateway lança falha imediata.
- Se a Certificação falhar ao verificar testes de unidade (`tests_ok = False`), a fábrica emite reprovação (`PROJECT READY = NO`).
- O `RepairLoop` reexecuta tarefas com falha até 3 vezes (`max_repair_attempts`) antes de classificar o projeto como `FAILED`.
- **Status de Homologação:** O teste E2E prévio alcançou o `PlannerAgent` e falhou na validação de agentes/comandos. As estabilizações subsequentes foram comprovadas por inspeção e análise estática, mas a execução do pipeline E2E completo permanece pendente de reexecução.
