# Qualidade e Certificação (Quality & Certification)

As camadas `m_quality` e `n_certification` são os guardiões finais de integridade e excelência técnica do AAF, garantindo que nenhum projeto gerado receba o selo de prontidão sem cumprir critérios rigorosos de conformidade.

## Quality Engine (`a_platform/m_quality/`)

Implementada em `a_quality_engine.py`, a ferramenta realiza auditoria estática e dinâmica do repositório gerado:

- **Dimensão Code:** Verifica a integridade sintática dos arquivos Python, densidade de código e ausência de construções defeituosas.
- **Dimensão Security:** Audita a ausência de vulnerabilidades conhecidas, chamadas inseguras e conformidade com a política de execução.
- **Dimensão Tests:** Inspeciona a existência real de arquivos de teste (`test_*.py`) e evidências de execução pelo `pytest`. Projetos que requerem testes mas não apresentam suíte comprovada têm pontuação zerada nesta dimensão.
- **Dimensão Documentation:** Valida a presença e consistência do `README.md` e manifestos exigidos pelas regras do Brain.

A aprovação exige uma pontuação global mínima (score >= 0.75) combinada com nota perfeita (1.0) nas dimensões críticas de estrutura e segurança.

## Certification Engine (`a_platform/n_certification/`)

O `CertificationEngine` (`a_certification_engine.py`) atua como a autoridade máxima de conformidade:

- Analisa o `QualityReport` e os resultados acumulados de validação e execução.
- Valores padrão e aprovações tácitas (`tests_ok = True` sem execução) são repudiados.
- Se os testes unitários falharem ou evidências documentais estiverem ausentes, o motor emite `CertificationResult(passed=False)`.

## Concessão de PROJECT READY

No `MasterOrchestrator`, o `ReadinessGate` avalia a tríade Validação + Qualidade + Certificação:

```
ValidationGate: SUCCESS
QualityScore: >= 0.75 (sem falhas estruturais)
Certification: PASSED (evidências reais comprovadas)
══════════════════════════════════════════════════════════
=> PROJECT READY = YES
```

Caso qualquer um dos critérios falhe, a concessão é negada (`PROJECT READY = NO`) e o projeto é marcado como `FAILED`.
