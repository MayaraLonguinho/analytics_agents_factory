# Orchestrator

## Responsibility
Master Orchestrator do AAF. Gerencia a execução serial e determinística do pipeline analítico e transições de fase.

## Path
`a_platform/o_orchestration/a_orchestrator.py`

## Inputs
[[AAF]]

## Outputs
Pipeline Execution & Telemetria (`PROJECT READY`)

## Integrations
- [[Discovery]]
- [[Dataset Profiling]]
- [[Brain]]
- [[Architecture]]
- [[Planner]]
- [[Project Factory]]
- [[Materializer]]
- [[Runtime]]
- [[Validation]]
- [[Repair Loop]]
- [[Quality]]
- [[Certification]]
- [[Project Ready]]

## Failure behavior
Interrompe a esteira, aciona [[Repair Loop]] se na fase de validação/execução, ou marca o projeto como `FAILED` se esgotadas as tentativas.
