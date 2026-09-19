# Skills

## Papel no Golden Path
Capacidades granulares e reutilizáveis de geração e processamento (ex: `dataset_profiling`, `sql_generation`, `etl_scripting`, `basic_coding`). São executadas sob contrato rígido pelo `SkillRegistry`, que valida parâmetros de entrada (`validate_input`), executa a lógica (`execute`) e valida a consistência da saída (`validate_output`).

## Posição no Fluxo
← **Anterior:** [[h_agents|Agents]]  
→ **Próximo:** [[j_mcps|MCPs]]

## Entrada e Saída
- **Entrada:** Dicionário de contexto da tarefa (`task_description`, `schema`, `dataset_path`, etc.).
- **Saída:** Dicionário de artefatos estruturados e validados (ex: `{"schema.sql": "..."}`, `{"etl.py": "..."}`).

## Integrações e Contratos
- Contrato Base: `a_platform/b_contracts/c_skill_contract.py` (`BaseSkill` / `SkillContract`)
- Catálogo e Descoberta: `a_platform/e_skills/skill_index.yaml` (`SkillIndex`)
- Roteamento Determinístico: `a_platform/e_skills/skill_router.py` (`SkillRouter`)
- Resolução e Execução: `a_platform/e_skills/skill_registry.py` (`SkillRegistry`)

## Referência Técnica
Para o catálogo completo, schemas de entrada/saída e validações, consulte [[d_skills|Subsistema de Skills]].
