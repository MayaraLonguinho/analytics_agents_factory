# Validation Gate

## Papel no Golden Path
Portão de validação multifacetado que avalia três critérios objetivos antes de permitir o avanço para a etapa de qualidade:
1. `ProjectValidation`: presença de ID de projeto, plano não vazio e materialização confirmada (`SUCCESS`);
2. `StructureValidation`: existência de todos os artefatos esperados no disco, arquivos não vazios e compilação passiva de sintaxe Python via `py_compile`;
3. `ExecutionValidation`: `ExecutionResult.status == "PASSED"`, código de retorno 0 e ausência de status `DENIED` ou `TIMEOUT`.

## Posição no Fluxo
← **Anterior:** [[o_runtime|Runtime]]  
→ **Próximo (Sucesso):** [[r_quality|Quality]]  
↳ **Desvio (Falha):** [[q_repair_loop|Repair Loop]]

## Entrada e Saída
- **Entrada:** `ExecutionContext` do projeto e `ExecutionResult` do runtime.
- **Saída:** `ValidationResult` com status (`PASSED` ou `FAILED`) e evidências detalhadas.

## Integrações e Contratos
- Componente: `a_platform/l_validation/a_validation_gate.py` (`ValidationGate`)
- Validador Estrutural: `a_platform/l_validation/b_structure_validation.py`
- Validador de Execução: `a_platform/l_validation/c_execution_validation.py`
- Validador de Projeto: `a_platform/l_validation/d_project_validation.py`

## Referência Técnica
Para detalhes das regras de compilação estática e validação de processos, consulte [[j_validation|Portões de Validação e Reparo]].
