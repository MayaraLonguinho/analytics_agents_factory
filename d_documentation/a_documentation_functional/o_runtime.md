# Runtime (Execution Runtime)

## Papel no Golden Path
Motor de execução dos comandos de teste e execução do projeto gerado (`ProjectRuntime`). Localizado em `a_platform/k_runtime/`, executa os processos com `shell=False`, timeout rigoroso de 120s e validação de segurança via `CommandPolicy`, gerando registros estruturados de evidência (`CommandExecutionResult[]`).

> [!IMPORTANT]
> **Distinção de Runtime:**
> - `a_platform/k_runtime/`: **Execution Runtime** — executa comandos e testes do projeto gerado.
> - `h_runtime/state/`: **Session Runtime State** — persiste o estado da sessão e pause/resume do próprio AAF.

## Posição no Fluxo
← **Anterior:** [[n_generated_projects|Generated Projects]]  
→ **Próximo:** [[p_validation|Validation]]

## Entrada e Saída
- **Entrada:** Comandos de execução planejados (`ProjectPlan.run_commands`) e diretório do projeto.
- **Saída:** `ExecutionResult` contendo status (`PASSED`/`FAILED`), código de retorno (`return_code`), `stdout`, `stderr` e a lista `commands` com evidências tipadas (`CommandExecutionResult`).

## Integrações e Contratos
- Motor: `a_platform/k_runtime/a_execution/a_runtime.py` (`ProjectRuntime`)
- Política: `a_platform/k_runtime/b_command_policy/a_policy.py` (`CommandPolicy`)
- Contrato: `a_platform/b_contracts/h_execution.py` (`ExecutionResult`, `CommandExecutionResult`)

## Referência Técnica
Para detalhes da sandbox, políticas de segurança e subprocessos, consulte [[i_runtime|Mecanismos de Runtime]] e [[h_command_policy|Política de Comandos]].
