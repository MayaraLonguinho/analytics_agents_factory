# Repair Loop

## Papel no Golden Path
Mecanismo de auto-recuperação acionado quando a execução ou a validação de uma tarefa falha. Constrói um pacote estruturado de evidências (`RepairContext` com stdout, stderr, código de retorno e erros de validação) e injeta no agente responsável para que este regenere o artefato defeituoso. O sucesso só é aceito após:
1. Regeneração do artefato;
2. Rematerialização em disco;
3. Reexecução dos comandos via Runtime com status `PASSED`;
4. Revalidação completa no `ValidationGate`.
Possui limite máximo estrito de 3 tentativas (`max_repair_attempts`).

## Posição no Fluxo
↳ **Acionado por:** Falha em [[p_validation|Validation Gate]]  
→ **Retorno em Sucesso:** [[r_quality|Quality]]  
→ **Retorno em Esgotamento:** Término com status `FAILED`

## Entrada e Saída
- **Entrada:** `ExecutionResult` falho, erros de validação e número da tentativa.
- **Saída:** Booleano indicando sucesso ou falha da tentativa de reparo, e atualização do estado do projeto.

## Integrações e Contratos
- Componente: `a_platform/o_orchestration/c_repair_loop.py` (`RepairLoop`)
- Contexto Tipado: `RepairContext`

## Referência Técnica
Para o fluxo detalhado de regeneração e critérios de reexecução, consulte [[j_validation|Portões de Validação e Reparo]].
