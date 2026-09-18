# Arquitetura

A Analytics Agents Factory (AAF) foi projetada como um **Modular Monolith**. Esta abordagem garante a simplicidade operacional, eliminando a sobrecarga de microserviços e infraestrutura distribuída na fase de MVP, ao mesmo tempo que mantém fronteiras lógicas estritas para futura escalabilidade.

## Camadas da Plataforma
A arquitetura é dividida em módulos organizados alfabeticamente para forçar previsibilidade e ordem de dependência:

- **b_contracts**: Contratos fundamentais Pydantic, exceções tipadas, interfaces e StateManager (`j_state_manager.py`).
- **c_brain**: O coração de conhecimento, repositório de regras de domínio (`b_rules`), decisões arquiteturais (`e_decisions`) e padrões (`c_patterns`). Representa o SSOT.
- **e_skills**: Capacidades granulares que os agentes executam, organizadas por categorias e registradas em `b_skills.yaml`.
- **f_mcps**: Protocolos de ação segura sob sandbox estrito (Filesystem, Docker, Database).
- **g_agents**: Implementações dos agentes nativos (Discovery, Architecture, Planner, Agent Factory) e especializados (Data, Database, Analytics, Testing, etc.).
- **h_factory**: Mecanismos de orquestração da fábrica lógica de projetos (`ProjectFactory`).
- **i_materializer**: Manipulador Físico de Arquivos e persistência em disco (`ArtifactMaterializer`).
- **j_llm_gateway**: Interface única para provedores de IA (OpenAI operacional via `gpt-4o-mini`, isolando SDK e roteamento).
- **k_runtime**: Ambiente seguro para execução de comandos do sistema de destino (`shell=False`, `CommandPolicy`).
- **l_validation**: Gates de validação funcional e verificação rigorosa de saída e evidências (`ValidationGate`).
- **m_quality**: Avaliação de componentes estáticos e evidências reais de qualidade e testes (`QualityEngine`).
- **n_certification**: Motor único de autorização de readiness de projetos (`CertificationEngine`).
- **o_orchestration**: Topologia de orquestração do pipeline completo (`MasterOrchestrator`) e ciclo de reparo (`RepairLoop`).

## Fluxo Principal de Execução

O pipeline da AAF é totalmente serial, sequencial e irreversível a menos que acionado pelo Loop de Reparo.

```
IDE Chat → IDE Adapter → Discovery → Dataset Profiling → Brain → Architecture → Planner → Project Factory → Materializer → Runtime → Validation → Repair → Quality → Certification → PROJECT READY
```

1. A entrada primária é feita através de adapters que despacham comandos para o Orchestrator.
2. O agente de Discovery levanta perfis e levanta a intenção.
3. Decisões arquiteturais são tomadas com base no SSOT (`c_brain`).
4. Um plano formalizado e atômico é criado pelo Planner, designando `Task.skills`.
5. A Factory instancia os agentes corretos baseados no plano e despacha execução (materialização via MCP).
6. Os outputs e códigos gerados sofrem bateria real de Runtime, Quality e Certification.
7. Se tudo passa sem falhas de evidência, o projeto é marcado como PROJECT READY.

## Princípios de Dependência
- Módulos inferiores não dependem dos superiores.
- Nenhuma inteligência LLM contorna o Gateway (`j_llm_gateway`).
- Nenhum agente contorna o plano traçado pelo `Planner`.
- O código gerado é materializado apenas pelo materializador designado usando a subcamada de MCP em ambiente Sandbox.
