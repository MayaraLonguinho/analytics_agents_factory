# Validation

## Responsibility
Gate de validação lógica e física. Avalia integridade de propriedades do projeto, presença de arquivos essenciais e evidências de execução dos comandos emitidos (`status == PASSED` e `return_code == 0`).

## Path
`a_platform/l_validation/a_validation_gate.py`

## Inputs
[[Runtime]], [[Orchestrator]]

## Outputs
ValidationResult com status de aprovação e diagnósticos de falha

## Integrations
- [[Repair Loop]]
- [[Quality]]

## Failure behavior
Reprova o avanço à fase de Qualidade e redireciona o fluxo para o [[Repair Loop]]. Se tentativas forem esgotadas, marca `FAILED`.
