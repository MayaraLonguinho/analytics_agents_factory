# Quality

## Responsibility
Motor de análise de qualidade estática e dinâmica. Inspeciona conformidade de código, testes, documentação e segurança, verificando invocações reais de ferramentas (`pytest`, `ruff`, etc.) via argv de `CommandExecutionResult`.

## Path
`a_platform/m_quality/a_quality_engine.py`

## Inputs
[[Validation]], [[Orchestrator]]

## Outputs
QualityReport detalhado por dimensão e nota agregada

## Integrations
- [[Certification]]

## Failure behavior
Reprova o relatório (`FAILED` ou `NOT_EXECUTED`) caso ferramentas mandatórias não tenham sido acionadas ou a nota fique abaixo do limiar (0.75).
