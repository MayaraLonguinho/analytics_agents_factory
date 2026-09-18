# Agentes e Responsabilidades Técnicas

Na Analytics Agents Factory, os agentes (`a_platform/g_agents`) são entidades especializadas que executam etapas específicas do ciclo de vida da fábrica, interagindo com o Brain, Skills e LLM Gateway sob contratos tipados.

## Separação de Papéis: IDE Chat vs Agents Nativos

- **IDE Chat:** Atua puramente como camada de transporte e interface de usuário. Não formula arquiteturas, não escreve arquivos de código do projeto analítico e não possui autorização para criar soluções de contorno.
- **Agents Nativos do AAF:** Todos os passos da geração pertencem exclusivamente aos agentes internos da plataforma sob o `MasterOrchestrator`.

## Agentes de Orquestração Principal

- **DiscoveryAgent (`b_discovery/`)**: Conduz o entendimento da demanda de entrada. Analisa o prompt, extrai dados de negócios e pausa a esteira de forma idempotente se faltar informação essencial (Fase `NEEDS_INPUT`).
- **ArchitectureAgent (`c_architecture/`)**: Lê o contexto estrito retornado pelo Brain e o profiling do dataset, projetando a decisão de arquitetura formal (`ArchitectureDecision`).
- **PlannerAgent (`d_planner/`)**: Agente SSOT da etapa de decomposição. Valida domínios, agentes, skills e MCPs autorizados, e aplica o preflight de `CommandPolicy` ao compor o `ProjectPlan`.

## Agentes Especializados (Factory Line)

Agentes focados em traduzir tarefas do plano em invocações de skills e geração de código:

- **DataAgent (`e_data/`)**: Profiling de dados, pipelines de ingestão e scripts ETL.
- **DatabaseAgent (`f_database/`)**: Esquemas relacionais, scripts DDL e migrações SQLite.
- **AnalyticsAgent (`g_analytics/`)**: Consultas analíticas avançadas, agregações e métricas de negócio.
- **BackendAgent (`h_backend/`) & FrontendAgent (`i_frontend/`)**: Componentes de API e interfaces quando autorizados pelo plano.
- **InfrastructureAgent (`j_infrastructure/`)**: Configuração de ambientes, `Dockerfile` e dependências.
- **ChatbotAgent (`k_chatbot/`)**: Integrações opcionais de conversação e RAG.
- **TestingAgent (`l_testing/`)**: Suítes de testes unitários automatizados com `pytest`.
- **DocumentationAgent (`m_documentation/`)**: Manifestos, guias de execução e documentação do projeto gerado.

## Instanciação e Contratos

- **AgentFactory (`n_factory/a_agent_factory.py`)**: Instancia dinamicamente apenas os agentes requisitados pelo plano, garantindo que agentes não autorizados sejam rejeitados.
- **BaseAgent (`a_platform/b_contracts/b_agent_contract.py`)**: Contrato base Pydantic que todos os agentes implementam obrigatoriamente.
