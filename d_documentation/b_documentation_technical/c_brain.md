# Brain (SSOT - Single Source of Truth)

O `Brain` (`a_platform/c_brain`) é o repositório central de conhecimento normativo e arquitetural da Analytics Agents Factory. Ele atua como a única fonte da verdade (SSOT) para agentes tomarem decisões determinísticas durante o planejamento e a geração de código.

## Estrutura Interna

O subsistema do Brain está organizado nas seguintes pastas:

- **a_context/**: Contexto operacional da fábrica, definições de baseline e escopo analítico.
- **b_rules/**: Regras obrigatórias de design, modelagem e verificação:
  - `c_architecture_rules.md`: Padrões arquiteturais exigidos (ex: Modular Monolith, proibição de microserviços em MVP).
  - `d_data_rules.md`: Modelagem de dados, convenções de nomenclatura e integridade.
  - `e_sql_rules.md`: Dialetos SQL suportados, exigência de CTEs e boas práticas de consulta.
  - `f_testing_rules.md`: Estrutura obrigatória para suítes de teste `pytest`.
  - `g_documentation_rules.md`: Templates padronizados para README e documentação técnica.
  - `h_project_ready_rules.md`: Critérios estritos para concessão do selo `PROJECT READY`.
- **c_patterns/**: Catálogo de padrões de código consolidados (ETL, SQL, testes, Dockerfile).
- **d_domains/**: Especializações de domínio analítico (`a_analytics.md`, `b_data_engineering.md`).
- **e_decisions/**: Registro de decisões arquiteturais históricas (ADRs).
- **f_adapters/** & **g_retrieval/**: Mecanismos de busca e recuperação de regras em tempo de execução.

## Status do Learning Engine

O módulo `h_learning_engine.py` é um componente experimental e encontra-se **estritamente fora do Golden Path** oficial. O pipeline principal da fábrica não executa nem depende do Learning Engine para alcançar o estado `PROJECT READY`.

## Relação com o Obsidian Graph

- Os arquivos Markdown do `Brain` utilizam wikilinks (`[[Link]]`) para permitir visualização relacional no Obsidian (`.obsidian/`).
- **Aviso Arquitetural:** O Obsidian Graph é estritamente uma camada de **visualização passiva** para humanos. Ele **NÃO é o SSOT** e não controla a lógica da plataforma.
- Os agentes e a fábrica leem diretamente os arquivos de `a_platform/c_brain/` via chamadas de sistema de arquivos e adaptadores internos.
