# Validação e Ciclo de Reparo (Validation & Repair Loop)

A camada `l_validation` e o módulo de reparo em `o_orchestration` constituem os mecanismos primários de garantia de que o código gerado e executado pelo `k_runtime` atende a todos os critérios funcionais antes de avançar para a avaliação de qualidade.

## Validation Gate (`a_platform/l_validation/`)

O `ValidationGate` (`a_validation_gate.py`) atua como inspetor de conformidade da execução:

- **Análise de Evidências Reais:** O gate não aceita conclusões presumidas. Ele inspeciona o `last_execution_result`, os códigos de retorno e os logs de execução emitidos pelo `RuntimeEngine`.
- **Detecção de Falhas Silenciosas:** Mesmo que um script retorne código zero, a saída textual é verificada contra erros sintáticos em Python, falhas de importação ou mensagens de erro em T-SQL/SQLite.
- **Ausência de Mocks:** Flags de aprovação padrão foram eliminadas da plataforma. Sem artefato palpável e evidência em log, o resultado de validação assume estritamente `passed = False`.

## Ciclo de Reparo (Repair Loop)

Quando o `ValidationGate` reprova a execução, o `MasterOrchestrator` intercepta o fluxo e direciona o processo para o `RepairLoop` (`a_platform/o_orchestration/b_repair_loop.py`):

1. **Diagnóstico da Falha:** O RepairLoop coleta os detalhes do erro (stderr, stacktrace, arquivos com problemas).
2. **Reformulação Dirigida:** Uma tarefa corretiva é criada para instruir o agente responsável a reparar os arquivos afetados sem descartar a fundação prévia do projeto.
3. **Limite de Tentativas:** O processo de correção automática repete-se por até 3 vezes (`max_repair_attempts = 3`).
4. **Resolução ou Falha Definitiva:**
   - Se o reparo for bem-sucedido e a validação passar, o projeto segue para a fase de Qualidade (`m_quality`).
   - Se as tentativas se esgotarem sem sucesso, a sessão transiciona para `FAILED` com relatório detalhado das causas da recusa.
