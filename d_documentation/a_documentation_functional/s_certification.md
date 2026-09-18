# Certification Engine

## Papel no Golden Path
Autoridade máxima e final de conformidade do projeto. Aplica a fórmula canônica de prontidão, validando a conjunção estrita de todas as fases:
$$\text{Discovery = COMPLETE} \land \text{Planning = COMPLETE} \land \text{Materialization = SUCCESS} \land \text{Execution = PASSED} \land \text{Validation = PASSED} \land \text{Quality = PASSED}$$
Se todas as condições forem rigorosamente verdadeiras, emite certificação de aprovação. Qualquer ausência, falha ou status divergente resulta em reprovação imediata.

## Posição no Fluxo
← **Anterior:** [[r_quality|Quality]]  
→ **Próximo:** [[t_project_ready|Project Ready]]

## Entrada e Saída
- **Entrada:** `ExecutionContext`, `ExecutionResult`, `ValidationResult` e `QualityResult`.
- **Saída:** `CertificationResult` com status (`PASSED` ou `FAILED`) e sumário de evidências.

## Integrações e Contratos
- Componente: `a_platform/n_certification/a_certification_engine.py` (`CertificationEngine`)
- Contrato: `a_platform/b_contracts/m_certification.py` (`CertificationResult`)

## Referência Técnica
Para a especificação formal dos gates de auditoria e regras de decisão, consulte [[k_quality_certification|Qualidade e Certificação]].
