# Agents

## Papel no Golden Path
Especialistas autônomos de execução (ex: `DataAgent`, `BaseAgent`). Cada agente executa a tarefa designada invocando habilidades (`Skills`) pelo `SkillRegistry`, ferramentas de ambiente (`MCPs`) pelo `MCPExecutor` e geração de código via `LLMGateway`.

## Posição no Fluxo
← **Anterior:** [[g_project_factory|Project Factory]]  
→ **Próximo:** [[i_skills|Skills]]

## Entrada e Saída
- **Entrada:** `ProjectTask`, enriquecida com o contexto de negócio, arquitetura e dataset.
- **Saída:** Objetos tipados `Artifact` contendo o código gerado, scripts de teste ou arquivos de configuração.

## Integrações e Contratos
- Base: `a_platform/g_agents/a_base/a_base_agent.py`
- Especialista: `a_platform/g_agents/e_data/a_data_agent.py`
- Fábrica: `a_platform/g_agents/n_factory/a_agent_factory.py`

## Referência Técnica
Para detalhes da hierarquia de classes, injeção de dependências e registro, consulte [[f_agents|Sistema de Agentes]].
