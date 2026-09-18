# Quality & Certification

A AAF emprega duas métricas terminais e não-negociáveis logo após o Runtime e a Validação Inicial, localizadas em `l_quality` e `m_certification`.

## Quality Engine (`l_quality/`)
Responsável por atribuir pontuação tangível baseado na extração material do projeto. Submete o repositório a escrutínios estáticos em `a_quality_engine.py`:
- **Code**: Confere as existências sintáticas de scripts e densidade.
- **Security**: Assegura que o Validation Gate devolveu relatório blindado e seguro para uso local ou produtivo.
- **Tests**: Escaneia assinaturas de suíte unitária (`test_*.py`). Sem suíte detectada em projeto que pede teste, o score desaba a zero, impossibilitando notas altas baseadas em ausência (falácia de aprovação nula).
- **Documentation**: Verifica conformidade rígida de manifestos e *Readmes* (ex: `README.md`).

A nota global exige um platô mínimo (>= 75%) acoplado obrigatoriamente a notas perfeitas (1.0) em estrutura, segurança e runtime para admitir um _PASS_.

## Certification Engine (`m_certification/`)
Atua como Juiz Supremo da plataforma em `a_certification_engine.py`. Analisa o *report* gerado por Quality e Validation. 

- Nenhum artifício _dummy_ é aceito. Defaults pregressos (`tests_ok = True`) foram duramente repudiados na arquitetura atual.
- Analisa profundamente os `metrics` instanciados em `QualityReport`.
- Falhas de teste ou falta de documentação implicam falha total: `CertificationResult(passed=False)`.

## O Veridito Final (PROJECT READY)
A etapa 11 da Topologia no `Orchestrator` (`ReadinessGate.evaluate`) intercepta a tríade Execution+Quality+Certification. A variável magna da telemetria `PROJECT_READY` assume `YES` **exclusiva e imutavelmente** quando todas as pontes relatam relatórios passantes atestados. Do contrário, a resposta permanece `NO` sob o status severo `FAILED`.
