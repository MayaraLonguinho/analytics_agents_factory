# Arquitetura Técnica

A Analytics Agents Factory (AAF) foi projetada como um **Modular Monolith**. Esta abordagem garante a simplicidade operacional, eliminando a sobrecarga de microserviços e infraestrutura distribuída na fase de MVP, ao mesmo tempo que mantém fronteiras lógicas estritas para futura escalabilidade.

## Camadas da Plataforma (`a_platform/`)

A arquitetura é dividida em módulos organizados alfabeticamente para forçar previsibilidade e ordem de dependência:

- **b_contracts**: Contratos fundamentais Pydantic, exceções tipadas, interfaces de agentes, skills, MCPs e o `StateManager` (`j_state_manager.py`).
- **c_brain**: O coração de conhecimento, repositório de regras de domínio (`b_rules`), decisões arquiteturais (`e_decisions`) e padrões (`c_patterns`). Representa o SSOT (Single Source of Truth).
- **e_skills**: Capacidades granulares que os agentes executam, organizadas por categorias e registradas no catálogo `b_skills.yaml`.
- **f_mcps**: Protocolos de ação segura sob sandbox estrito (Filesystem, Docker, Database SQLite).
- **g_agents**: Implementações dos agentes nativos de orquestração (Discovery, Architecture, Planner, Agent Factory) e especializados (Data, Database, Analytics, Testing, etc.).
- **h_factory**: Mecanismos de orquestração da fábrica lógica de projetos (`ProjectFactory`).
- **i_materializer**: Manipulador físico de arquivos e persistência estruturada em disco (`ArtifactMaterializer`).
- **j_llm_gateway**: Interface única para provedores de IA (OpenAI operacional via `gpt-4o-mini`, isolando SDK e roteamento).
- **k_runtime**: Execution Runtime seguro para comandos dos projetos gerados (`shell=False`, `CommandPolicy`).
- **l_validation**: Gates de validação funcional e verificação rigorosa de evidências de execução (`ValidationGate`).
- **m_quality**: Avaliação de componentes estáticos e evidências reais de qualidade e testes (`QualityEngine`).
- **n_certification**: Motor único de autorização de readiness de projetos (`CertificationEngine`).
- **o_orchestration**: Topologia de orquestração do pipeline completo (`MasterOrchestrator`) e ciclo de reparo (`RepairLoop`).

## Princípios de Dependência

1. **Unidirecionalidade**: Módulos inferiores não dependem de módulos superiores.
2. **Isolamento de LLM**: Nenhuma chamada ao modelo de linguagem contorna o `j_llm_gateway`.
3. **Determinismo no Planejamento**: Nenhum agente executa tarefas ou skills fora do plano traçado pelo `Planner`.
4. **Sandbox de Escrita**: O código gerado é materializado exclusivamente na pasta `e_generated_projects/` através do Filesystem MCP.
5. **Diferenciação de Runtimes**:
   - `a_platform/k_runtime/` executa comandos dos projetos gerados.
   - `h_runtime/state/` armazena o estado de sessão e pause/resume do próprio AAF.

## Pipeline Sequencial de Orquestração

O pipeline da AAF é totalmente serial, sequencial e irreversível a menos que acionado pelo Loop de Reparo:

```
Request → Discovery → Dataset Profiling → Brain → Architecture → Planner → Project Factory → Agents → Skills → MCPs → LLM Gateway → Artifact → Materializer → Generated Projects → Runtime → Validation → Repair Loop → Quality → Certification → Project Ready
```
