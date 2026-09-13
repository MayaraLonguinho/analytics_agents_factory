# Arquitetura

A Analytics Agents Factory (AAF) foi projetada como um **Modular Monolith**. Esta abordagem garante a simplicidade operacional, eliminando a sobrecarga de microserviços e infraestrutura distribuída na fase de MVP, ao mesmo tempo que mantém fronteiras lógicas estritas para futura escalabilidade.

## Camadas da Plataforma
A arquitetura é dividida em módulos organizados alfabeticamente para forçar previsibilidade e ordem de dependência:

- **a_core**: Contratos fundamentais, exceções tipadas, configuração e estrutura de sessão (SessionContext e StateManager). É a camada mais básica, sem dependências de outras áreas.
- **b_interfaces**: Adaptadores de entrada. Centraliza a CLI (`c_commands.py`) e a integração com a IDE (Session Adapter).
- **c_brain**: O coração de conhecimento, repositório de regras de domínio, decisões arquiteturais e memória estrita em Markdown e metadados. Representa o SSOT (Single Source of Truth) para o modelo operacional.
- **d_agents**: Implementações dos agentes principais (Discovery, Architecture, Planner, Agent Factory) e especializados (Data, Database, Frontend, etc.).
- **e_skills**: Capacidades que os agentes executam, organizadas por categorias, sem implementações "mockadas". Interagem obrigatoriamente através da `LLMGateway`.
- **f_mcp**: Extensões de ação no mundo real, operando sob *sandbox* estrito (Filesystem, Docker seguro, Database com filtros).
- **g_llm_gateway**: Interface única para provedores de IA (OpenAI, Gemini, Anthropic), isolando a lógica de SDK e roteamento.
- **h_factory**: Mecanismos de geração de projetos (`ProjectFactory`) e o materializador de disco (`ArtifactMaterializer`).
- **i_domains**: Repositórios canônicos para domínios de geração de projetos (como `analytics`, `data_engineering`).
- **j_runtime**: Ambiente seguro para execução de comandos do sistema de destino e telemetria de saúde de execução.
- **k_validation**: Gates de validação funcional e verificação rigorosa de saída e logs.
- **l_quality** e **m_certification**: Avaliação de componentes estáticos (Testes, Code Quality, Documentação) e emissão de atestado de que o projeto atendeu aos requisitos.
- **n_orchestration**: Topologia de orquestração do pipeline completo, acionando o Repair Loop no caso de falhas nas verificações.

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
- Nenhuma inteligência LLM contorna o Gateway (`g_llm_gateway`).
- Nenhum agente contorna o plano traçado pelo `Planner`.
- O código gerado é materializado apenas pelo materializador designado usando a subcamada de MCP em ambiente Sandbox.
