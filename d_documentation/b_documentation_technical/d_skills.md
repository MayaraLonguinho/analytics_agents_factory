# Skills (Habilidades Técnicas)

As *Skills* (`a_platform/e_skills`) representam o arcabouço funcional com o qual os agentes realizam tarefas práticas no AAF. Cada skill encapsula lógica nativa em Python e/ou interações com o `j_llm_gateway` sob um contrato fortemente tipado.

## Categorias e Estrutura

As skills estão organizadas em subdiretórios funcionais:

1. **a_dataset_profiling**: Profiling determinístico de dados utilizando Pandas (`DatasetProfilingSkill`).
2. **b_etl**: Scripts de extração, transformação, limpeza e normalização (`EtlScriptingSkill`).
3. **c_sql**: Geração de esquemas DDL, consultas analíticas com CTEs e agregações (`SqlGenerationSkill`).
4. **d_analytics**: Cálculos analíticos e métricas de negócio (`AnalyticsCalculationSkill`).
5. **e_quality**: Geração de suítes de testes unitários automatizados com `pytest` (`TestingSkill`).
6. **f_documentation**: Geração de documentação de projeto, arquitetura e manifestos (`DocumentationSkill`).
7. **g_optional**: Habilidades opcionais para escopos estendidos (`DockerSkill`, `BackendSkill`, etc.).
8. **h_registry**: Catálogo e gerenciador de resolução de skills:
   - `b_skills.yaml`: Declaração formal de todas as skills, suas entradas, saídas e metadados.
   - `a_skill_registry.py`: Registry que valida e instancia skills em tempo de execução.

## Contratos e Execution Contract

Todas as skills implementam o contrato base definido em `a_platform/b_contracts/c_skill_contract.py` (`SkillContract`, `SkillResult`).

### O Fluxo Inviolável de Execução

```
Planner → Task.skills → Agent → SkillRegistry → Execução
```

1. O **PlannerAgent** define formalmente quais skills são necessárias para cada tarefa ao compor o `ProjectPlan`.
2. O **Agente designado** (ex: `DataAgent`) recebe a tarefa contendo a lista `Task.skills`.
3. O agente **NÃO injeta** skills por iniciativa própria; ele resolve e executa rigorosamente as skills especificadas através do `SkillRegistry`.
4. Os resultados são encapsulados em instâncias de `SkillResult` para posterior composição de artefatos.
