# Agentes e Responsabilidades

A AAF delega trabalho atômico a *Agents*. Eles são categorizados de acordo com suas atribuições dentro do ciclo do projeto.

## Agentes Principais de Orquestração
Agentes fundamentais gerando planos lógicos que a fábrica consome:
- **DiscoveryAgent**: Conduz o entendimento da demanda de entrada. Analisa o prompt, extrai dados de negócios e solicita (ou paralisa) a esteira se um detalhe chave for faltante (Fase `NEEDS_INPUT`).
- **ArchitectureAgent**: Lê o contexto estrito retornado pelo Brain e projeta um *Pattern* em alto nível sem tocar no código real.
- **PlannerAgent**: Agente SSOT da etapa de decomposição. A ele cabe o dever de criar o objeto `ProjectPlan` distribuindo estritamente as Listas de Skills adequadas.

## Agentes Especializados (Factory Line)
Entidades reativas focadas em traduzir tarefas abstratas em chamadas literais da `LLMGateway` conectando às Skills (em `a_platform/d_agents`):
- **DataAgent**: Focado nas execuções de profiling de dataset e modelagem ETL primária.
- **DatabaseAgent**: Geração de esquemas DDL (Database Definition Language).
- **AnalyticsAgent**: Construção analítica avançada e cálculos SQL e agregações.
- **BackendAgent / FrontendAgent**: Para pipelines de apresentação e serviços conectivos.
- **InfrastructureAgent / DockerSkill**: Scripts de orquestração IAC e recipes.
- **ChatbotAgent**: Habilidades opcionais para Chatbot e integrações RAG/LangChain.
- **TestingAgent**: Geração puramente guiada aos Testes Unitários/Integração.
- **DocumentationAgent**: Refino do *README.md* pós arquitetura.

## Agentes Condicionais e Factory
- Apenas os agentes ditados pelo Planner (via Tasks) ganham instância real em tempo de execução através do `m_agent_factory/a_agent_factory.py`.
- Todas as definições de Agent Contracts respeitam a fachada `d_project_contract.py` mantendo os Handlers centralizados e os Agents puros.
