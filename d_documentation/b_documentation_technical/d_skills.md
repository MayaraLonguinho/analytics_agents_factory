# Subsistema de Skills — Catálogo, Indexação e Roteamento

As *Skills* (`a_platform/e_skills`) representam as capacidades granulares e reutilizáveis utilizadas pelos Agents para realizar tarefas no Analytics Agents Factory (AAF). Cada skill obedece ao `SkillContract`, executando o ciclo estrito:
`validate_input() → execute() → validate_output()`.

---

## 1. Fluxo de Descoberta e Roteamento Multi-Skill

O AAF implementa **Progressive Disclosure**, **Lazy Loading** e **Multi-Skill Capability Routing**. Uma única tarefa pode exigir múltiplas capabilities (`1..N`), que são resolvidas deterministicamente pelo `SkillRouter` em uma `SkillSelection` ordenada e deduplicada, respeitando dependências entre skills (`depends_on`), permissões de domínio (`allowed_skills`) e permissões do agente (`allowed_agents`). O `SkillRegistry` realiza o carregamento sob demanda de cada skill apenas no instante de sua execução isolada:

```text
Project
  ↓
Planner (Tasks [1..N])
  ↓
Task (Capabilities [1..N], Preferred Skills [1..N])
  ↓
Agent (BaseAgent)
  ↓
SkillRouter.route_selection()
  ↓
SkillIndex (Catálogo YAML compacto + depends_on)
  ↓ (Filtros de Domain allowed_skills e Agent allowed_agents)
SkillSelection [1..N] (Deduplicação + Ordenação Topológica por Dependências)
  ↓
SkillRegistry (Lazy loader sob demanda por skill_id)
  ↓
Skill 1 (carregamento sob demanda) → validate_input() → execute() → validate_output() → Artifact 1
  ↓
Skill 2 (carregamento sob demanda) → validate_input() → execute() → validate_output() → Artifact 2
  ↓
Skill N ...
```

### Níveis de Progressive Disclosure:
- **Nível 1 (Catálogo Compacto):** `SkillIndex` disponibiliza apenas metadados essenciais (`id`, `category`, `description`, `capabilities`, `allowed_agents`, `depends_on`).
- **Nível 2 (SkillSelection & Selected Skill):** `SkillSelection` mapeia o plano de execução (`skill_id`, `capability`, `order`, `dependencies`), deferindo a carga de cada `SKILL.md` e classe concreta até sua execução específica.
- **Nível 3 (Recursos Extras de Execução):** Assets, templates ou scripts específicos carregados exclusivamente durante o ciclo de vida da skill ativa, sendo descarregados ao final.

---

## 2. Catálogo Canônico de Skills

| Skill ID | Category | Purpose | Location | Allowed Agents |
|---|---|---|---|---|
| `dataset-profiling` | `dataset` | Analisa estrutura, schema, tipos e duplicatas físicas do dataset | `b_dataset/profiling` | `DiscoveryAgent`, `DataAgent`, `AnalyticsAgent` |
| `data-ingestion` | `dataset` | Ingestão robusta e leitura de arquivos ou bancos de dados | `b_dataset/ingestion` | `DataAgent` |
| `data-cleaning` | `dataset` | Limpeza, remoção de caracteres espúrios e deduplicação | `b_dataset/cleaning` | `DataAgent`, `AnalyticsAgent` |
| `data-transformation` | `dataset` | Transformações estruturadas, regras de negócio e tipagem | `b_dataset/transformation` | `DataAgent`, `AnalyticsAgent` |
| `dataset-validation` | `dataset` | Validação estrutural de schema e integridade do input | `b_dataset/validation` | `DataAgent`, `TestingAgent` |
| `exploratory-data-analysis` | `analytics` | Análise exploratória descritiva de dados estruturados (EDA) | `c_analytics/exploratory_data_analysis` | `AnalyticsAgent`, `DataAgent` |
| `statistical-analysis` | `analytics` | Análise estatística descritiva, correlações e distribuições | `c_analytics/statistical_analysis` | `AnalyticsAgent` |
| `metrics-analysis` | `analytics` | Cálculo e agregação de métricas de negócio e KPIs | `c_analytics/metrics_analysis` | `AnalyticsAgent`, `DatabaseAgent` |
| `data-visualization` | `analytics` | Geração de gráficos e plots visuais de dados | `c_analytics/data_visualization` | `AnalyticsAgent` |
| `feature-engineering` | `analytics` | Criação, encoding e escalonamento de features | `c_analytics/feature_engineering` | `AnalyticsAgent` |
| `feature-selection` | `analytics` | Seleção de variáveis preditivas e redução de dimensionalidade | `c_analytics/feature_selection` | `AnalyticsAgent` |
| `model-training` | `analytics` | Treinamento e validação cruzada de modelos de ML | `c_analytics/model_training` | `AnalyticsAgent` |
| `model-evaluation` | `analytics` | Avaliação de performance de modelos com relatórios e matrizes | `c_analytics/model_evaluation` | `AnalyticsAgent`, `TestingAgent` |
| `prediction` | `analytics` | Inferência e previsões em lote utilizando modelos treinados | `c_analytics/prediction` | `AnalyticsAgent` |
| `etl-pipeline` | `data_engineering` | Pipeline de ETL determinístico e executável em Python | `d_data_engineering/etl_pipeline` | `DataAgent` |
| `sql-analytics` | `data_engineering` | SQL analítico compatível com a stack (CTEs, agregações) | `d_data_engineering/sql_analytics` | `AnalyticsAgent`, `DatabaseAgent`, `DataAgent` |
| `sql-optimization` | `data_engineering` | Otimização de queries SQL e planos de execução | `d_data_engineering/sql_optimization` | `DatabaseAgent`, `AnalyticsAgent` |
| `dimensional-modeling` | `data_engineering` | Modelagem dimensional (Star Schema, fatos e dimensões) | `d_data_engineering/dimensional_modeling` | `DatabaseAgent`, `DataAgent` |
| `analytics-engineering` | `data_engineering` | Modelagem analítica modular em camadas (staging, marts) | `d_data_engineering/analytics_engineering` | `AnalyticsAgent`, `DataAgent` |
| `pipeline-observability` | `data_engineering` | Logging estruturado e métricas de execução do pipeline | `d_data_engineering/pipeline_observability` | `DataAgent`, `TestingAgent` |
| `technical-documentation`| `development` | Documentação técnica, especificações e dicionários de dados | `e_development/technical_documentation` | `DocumentationAgent` |
| `readme-generation` | `development` | README.md oficial com comandos de execução e testes | `e_development/readme_generation` | `DocumentationAgent` |
| `architecture-documentation` | `development` | Documentação arquitetural e diagramas de componentes | `e_development/architecture_documentation` | `DocumentationAgent` |
| `data-quality` | `quality` | Asserções de integridade, completude e qualidade de dados | `f_quality/data_quality` | `DataAgent`, `TestingAgent`, `AnalyticsAgent` |
| `code-quality` | `quality` | Testes automatizados via Pytest e validação de código | `f_quality/code_quality` | `TestingAgent` |
| `dependency-quality` | `quality` | Pinagem e auditoria de dependências em requirements.txt | `f_quality/dependency_quality` | `TestingAgent`, `DocumentationAgent` |

---

## 3. Ordem de Prioridade no Roteamento

O `SkillRouter` seleciona deterministicamente a Skill correta nesta ordem:
1. `preferred_skill` / `preferred_skills` explícita e autorizada;
2. `skill_id` explícito e autorizado;
3. `capability` / `capabilities` exatas declaradas na tarefa;
4. Verificação de `allowed_skills` do Domínio (`b_domains.yaml`);
5. Verificação de `allowed_agents` da Skill (`skill_index.yaml`);
6. Match por capabilities relacionadas e sinônimos canônicos;
7. Match por triggers/descrição de tarefas.

---

## 4. Multi-Skill Selection e Resolução de Dependências

O método `SkillRouter.route_selection(...)` (e seu alias `route_many(...)`) orquestra o roteamento para tarefas que exigem `1..N` capabilities:

1. **Resolução de Capabilities:** Para cada capability fornecida, o `SkillIndex` é consultado para encontrar a skill correspondente.
2. **Filtragem de Guardrails:** Validações rigorosas de `allowed_skills` (do Domínio) e `allowed_agents` (da Skill). Rejeições e skills não encontradas disparam `SkillRoutingError` explícito (sem fallbacks falsos).
3. **Deduplicação Inteligente:** Se múltiplas capabilities apontam para a mesma skill (ex: `data-cleaning` e `deduplication` -> `data-cleaning`), a skill é agendada uma única vez na `SkillSelection`, agregando as capabilities atendidas.
4. **Ordenação Topológica (`depends_on`):** O `SkillRouter` lê as dependências estruturais declaradas em `skill_index.yaml` e organiza as skills em ordem determinística de execução (`order: 1..N`). Dependências satisfeitas por etapas prévias não são duplicadas.
5. **Lazy Loading pelo `SkillRegistry`:** A `SkillSelection` contém apenas identificadores leves (`skill_ids`, `items`). O carregamento de código e prompts de cada skill só ocorre no instante exato em que `SkillRegistry.run_skill(...)` é chamado durante a execução da tarefa pelo Agente.

