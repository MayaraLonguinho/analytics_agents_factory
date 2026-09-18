# Skills (Habilidades)

As *Skills* (localizadas em `a_platform/e_skills`) compõem o arcabouço tangível que os Agentes possuem para resolver as tarefas. Skills são blocos operacionais reais executando lógica nativa ou invocando o `j_llm_gateway` sob um contrato forte de sistema.

## Categorias e Hierarquias
As habilidades estão organizadas de forma determinística em:
1. `a_dataset_profiling`: Análise física e determinística de fontes via Pandas (`DatasetProfilingSkill`).
2. `b_etl`: Scripts de extração, limpeza e normalização (`EtlScriptingSkill`).
3. `c_sql`: Modelagem de consultas relacionais, CTEs e agregações (`SqlGenerationSkill`).
4. `d_analytics`: Métricas de negócio e cálculo analítico (`AnalyticsCalculationSkill`).
5. `e_quality`: Geração e parametrização de suítes de teste automatizado (`TestingSkill`).
6. `f_documentation`: Geração de manifestos, arquitetura de projeto e guias (`DocumentationSkill`).
7. `g_optional`: Capacidades auxiliares opcionais (`DockerSkill`, `BackendSkill`, etc.).
8. `h_registry`: Catálogo oficial de declarações (`b_skills.yaml`) e despachante (`a_skill_registry.py`).

## Registry, Declarations e Contratos
- `a_platform/e_skills/h_registry/b_skills.yaml`: Catálogo SSOT onde todas as skills são formalmente declaradas com suas assinaturas e schemas.
- `a_platform/b_contracts/c_skill_contract.py`: Contrato Pydantic base (`SkillContract`, `SkillResult`).
- `a_platform/e_skills/h_registry/a_skill_registry.py`: Motor de registro e resolução de instâncias de skills em tempo de execução.

## O Fluxo Inviolável
**Fluxo:** `Planner → Task.skills → Agent → SkillRegistry`
O Planner é a entidade com autoridade para definir qual lista de `skills` preencherá os metadados de uma tarefa gerada. Agentes (ex: `DataAgent`) NÃO injetam skills arbitrariamente. Os Agentes repassam e executam rigidamente os requisitos do Planner utilizando os contratos do `SkillRegistry` para gerar o conteúdo real.
