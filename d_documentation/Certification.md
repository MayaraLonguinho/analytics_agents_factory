# Certification

## Responsibility
Juiz supremo e Single Source of Truth para autorização de readiness. Avalia a tríade de execução, validação e qualidade, recusando categoricamente aprovações passivas ou flags dummy.

## Path
`a_platform/n_certification/a_certification_engine.py`

## Inputs
[[Quality]], [[Orchestrator]]

## Outputs
CertificationResult atestado formalmente (`passed=True/False`)

## Integrations
- [[Project Ready]]

## Failure behavior
Emite veredito negativo (`passed=False`), forçando o status do projeto para `FAILED` e `PROJECT READY = NO`.
