# Skills (Habilidades)

As *Skills* (localizadas em `a_platform/e_skills`) compõem o arcabouço tangível que as LLMs e Agentes possuem para resolver as tarefas. Skills são blocos operacionais reais invocando `g_llm_gateway` sob um contrato forte de sistema.

## Categorias e Hierarquias
As habilidades foram isoladas semanticamente para facilidade cognitiva e orquestração:
1. `a_dataset`: Engloba processos de `c_profiling` (Dataset Profiling, para explorar os CSV/Fontes).
2. `b_data_engineering`: Ações duras como `EtlScriptingSkill`.
3. `d_analytics`: Criação de views, materializações matemáticas e `SqlGenerationSkill`.
4. `e_optional_capabilities/a_development/`: Engloba lógicas contextuais da aplicação final (`FrontendSkill`, `BackendSkill`, `DocumentationSkill`, `DockerSkill` etc).
5. `f_quality`: Habilidades voltadas ao escrutínio interno e baterias rigorosas como `TestingSkill`.

## Registry, Declarations e Contratos
- `h_declarations/a_skills.yaml`: Todas as skills devem ser formalmente declaradas e expor suas expectativas de Input/Output Schema.
- `i_contracts/a_skill_contract.py`: Garante que cada módulo de skill possua método `.execute()` compatível.
- `g_registry/j_skill_registry.py`: Motor local que registra em memória a skill solicitada com seu Handler.

## O Fluxo Inviolável
**Fluxo:** `Planner → Task.skills → Agent → SkillRegistry`
O Planner é a entidade com autoridade para definir qual lista de `skills` preencherá os metadados de uma tarefa gerada. Agentes (ex: `DataAgent`) NÃO injetam skills arbitrariamente ("mock-overwrites"). Os Agentes repassam e executam rigidamente os requisitos do Planner utilizando os contratos do `SkillRegistry` para gerar o conteúdo real.
