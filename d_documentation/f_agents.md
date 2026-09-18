# Agentes e Responsabilidades

A AAF delega trabalho atômico a *Agents*. Eles são categorizados de acordo com suas atribuições dentro do ciclo do projeto.

## Separação de Papéis: IDE Chat vs Agents Nativos
- **IDE Chat:** Atua puramente como camada de transporte e interface de usuário. Não formula arquiteturas, não escreve arquivos de código do projeto analítico e não possui autorização para criar soluções de contorno.
- **Agents Nativos do AAF:** Todos os passos da geração pertencem exclusivamente aos agentes internos da plataforma (`a_platform/g_agents`).

## Agentes Principais de Orquestração
Agentes fundamentais gerando planos lógicos que a fábrica consome:
- **DiscoveryAgent**: Conduz o entendimento da demanda de entrada. Analisa o prompt, extrai dados de negócios e pausa a esteira de forma idempotente se faltar informação essencial (Fase `NEEDS_INPUT`).
- **ArchitectureAgent**: Lê o contexto estrito retornado pelo Brain e DatasetProfile, projetando a decisão de arquitetura formal (`ArchitectureDecision`).
- **PlannerAgent**: Agente SSOT da etapa de decomposição. Valida domínios, agentes, skills e MCPs autorizados, e aplica o preflight de `CommandPolicy` ao compor o `ProjectPlan`.

## Agentes Especializados (Factory Line)
Entidades focadas em traduzir tarefas abstratas em chamadas literais da `LLMGateway` conectando às Skills (em `a_platform/g_agents`):
- **DataAgent**: Focado nas execuções de profiling de dataset e modelagem ETL primária.
- **DatabaseAgent**: Geração de esquemas DDL (Database Definition Language).
- **AnalyticsAgent**: Construção analítica avançada e cálculos SQL e agregações.
- **BackendAgent / FrontendAgent**: Para pipelines de apresentação e serviços conectivos (quando autorizados).
- **InfrastructureAgent**: Scripts de containerização e recipes.
- **ChatbotAgent**: Habilidades opcionais para Chatbot e integrações RAG.
- **TestingAgent**: Geração puramente guiada aos Testes Automatizados com `pytest`.
- **DocumentationAgent**: Refino de documentação e manifestos do projeto.

## Agentes Condicionais e Factory
- Apenas os agentes previstos no plano ganham instância real em tempo de execução através de `a_platform/g_agents/n_factory/a_agent_factory.py`.
- Todas as definições de contratos de agentes respeitam a interface `a_platform/b_contracts/b_agent_contract.py`.
