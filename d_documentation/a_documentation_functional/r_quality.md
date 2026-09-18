# Quality Engine

## Papel no Golden Path
Motor de qualidade física do código gerado. Avalia os registros estruturados de execução (`CommandExecutionResult[]`) para garantir conformidade em três dimensões:
1. `CodeQuality`: execução de linter/formatador (`flake8` ou `ruff`) com exit code 0;
2. `SecurityQuality`: execução de análise de segurança estática (`bandit`) com exit code 0;
3. `DependencyQuality`: execução de integridade de dependências (`pip check`) com exit code 0.
A ausência de qualquer uma das ferramentas obrigatórias gera status `NOT_EXECUTED`, considerado falha impeditiva (ausência de evidência = falha).

## Posição no Fluxo
← **Anterior:** [[p_validation|Validation Gate]] (ou [[q_repair_loop|Repair Loop]])  
→ **Próximo:** [[s_certification|Certification]]

## Entrada e Saída
- **Entrada:** `ValidationResult` anterior (obrigatoriamente `PASSED`) e `ExecutionResult.commands` contendo as evidências físicas de subprocessos.
- **Saída:** `QualityResult` com status (`PASSED` ou `FAILED`) e evidências dos gates satisfeitos.

## Integrações e Contratos
- Componente: `a_platform/m_quality/a_quality_engine.py` (`QualityEngine`)
- Subgates: `b_code_quality.py`, `c_security_quality.py` e `d_dependency_quality.py`
- Contrato: `a_platform/b_contracts/l_quality.py` (`QualityResult`)

## Referência Técnica
Para detalhes da avaliação baseada em evidência física e executáveis permitidos, consulte [[k_quality_certification|Qualidade e Certificação]].
