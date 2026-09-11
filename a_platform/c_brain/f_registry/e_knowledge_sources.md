# Fontes de Conhecimento

## Visão Geral

O Knowledge Registry organiza as fontes de conhecimento em três tipos principais: Internal Knowledge, External Knowledge e Generated Knowledge. Cada tipo tem características específicas e formas de utilização pelos Agents.

## Internal Knowledge

### Estrutura

```
internal_knowledge/
├── architecture/              # Arquitetura do sistema
├── patterns/                  # Padrões de design
├── prompts/                   # Prompts para IA
├── rules/                      # Regras de desenvolvimento
├── examples/                   # Exemplos de código
├── best_practices/             # Melhores práticas
├── decision_log/               # Histórico de decisões
├── adr/                        # Architecture Decision Records
├── obsidian/                   # Notas com links bidirecionais
├── graphify/                   # Visualizações
├── markdown/                   # Documentação Markdown
├── json/                       # Estruturas JSON
└── personal_finance_flow/      # Conhecimento de projeto de referência
    ├── architecture/
    ├── backend/
    ├── frontend/
    ├── database/
    ├── etl/
    ├── analytics/
    ├── business_rules/
    ├── patterns/
    ├── prompts/
    └── examples/
```

### Categorias

#### Arquitetura
- Visão geral e princípios de design
- Componentes detalhados do sistema
- Padrões arquiteturais implementados
- Decisões arquiteturais (ADRs)

#### Padrões
- Clean Architecture
- SOLID Principles
- Design Patterns GoF
- Padrões específicos do projeto

#### Prompts
- System prompts para Agents
- Prompts para tarefas específicas
- Templates de prompts reutilizáveis

#### Regras
- Regras de código (PEP 8, type hints, docstrings)
- Regras de arquitetura
- Regras de desenvolvimento
- Regras de documentação

#### Exemplos
- Exemplos de código representativos
- Snippets reutilizáveis
- Configurações de exemplo
- Casos de uso implementados

#### Personal Finance Flow
- Conhecimento específico do projeto de referência
- Padrões de backend, frontend, database, ETL, analytics
- Regras de negócio
- Estruturas validadas em produção

### Como os Agents Utilizam

**Architecture Agent**:
- Consulta `architecture/` para compreender arquitetura do sistema
- Consulta `adr/` para decisões arquiteturais anteriores
- Consulta `patterns/` para aplicar padrões arquiteturais

**Backend Agent**:
- Consulta `personal_finance_flow/backend/` para padrões de backend
- Consulta `examples/` para exemplos de implementação
- Consulta `rules/` para regras de código

**Frontend Agent**:
- Consulta `personal_finance_flow/frontend/` para padrões de frontend
- Consulta `patterns/` para padrões de design
- Consulta `examples/` para exemplos de componentes

**ETL Agent**:
- Consulta `personal_finance_flow/etl/` para padrões de ETL
- Consulta `patterns/` para padrões de pipeline
- Consulta `best_practices/` para melhores práticas

**Analytics Agent**:
- Consulta `personal_finance_flow/analytics/` para padrões de analytics
- Consulta `examples/` para exemplos de dashboards
- Consulta `patterns/` para padrões de visualização

## External Knowledge

### Estrutura

```
external_knowledge/
├── anthropic/                 # Documentação da Anthropic
├── awesome_agent_skills/     # Catálogo de skills
├── github_examples/          # Exemplos de projetos
├── mcp_examples/             # Exemplos de MCP
├── llm_patterns/             # Padrões LLM
└── documentation/            # Documentação oficial
```

### Categorias

#### Anthropic
- Documentação oficial da API da Anthropic
- Informações sobre modelos Claude
- Melhores práticas de uso
- Prompt engineering
- Limites e rate limits
- Segurança e conformidade

#### Awesome Agent Skills
- Catálogo de skills disponíveis
- Implementações de referência
- Padrões de skills
- Best practices para desenvolvimento
- Casos de uso

#### GitHub Examples
- Repositórios de referência
- Padrões de projeto
- Implementações exemplares
- Arquiteturas bem-sucedidas
- Configurações e CI/CD

#### MCP Examples
- Documentação do protocolo MCP
- Exemplos de MCP Servers
- Padrões de implementação
- Interações com serviços
- Best practices

#### LLM Patterns
- Padrões arquiteturais para LLM
- Prompt patterns
- Chain of Thought
- RAG patterns
- Agent patterns
- Tool use patterns

#### Documentation
- FastAPI
- Pydantic
- SQLAlchemy
- Pandas
- NumPy
- Scikit-learn
- PostgreSQL
- Docker
- GitHub Actions
- Python (PEPs)

### Como os Agents Utilizam

**Todos os Agents**:
- Consultam `documentation/` para documentação de bibliotecas utilizadas
- Consultam `anthropic/` para integração com Claude
- Consultam `llm_patterns/` para padrões de implementação LLM

**ETL Agent**:
- Consulta `documentation/` para Pandas, SQLAlchemy
- Consulta `github_examples/` para exemplos de pipelines

**ML Agent**:
- Consulta `documentation/` para Scikit-learn, NumPy
- Consulta `llm_patterns/` para padrões de ML

**Architecture Agent**:
- Consulta `mcp_examples/` para padrões de MCP
- Consulta `llm_patterns/` para arquiteturas LLM

## Generated Knowledge

### Estrutura

```
generated_knowledge/
├── reports/           # Relatórios de execução
├── analyses/          # Análises de dados
├── plans/             # Planos de execução
├── decisions/         # Logs de decisões
├── metrics/           # Métricas e estatísticas
├── summaries/         # Sumarizações
├── insights/          # Insights gerados
└── recommendations/   # Recomendações
```

### Categorias

#### Reports
- Relatórios de execução de workflows
- Relatórios de performance
- Relatórios de erros
- Relatórios de utilização

#### Analyses
- Análises exploratórias de dados
- Análises de tendências
- Análises de padrões
- Análises comparativas

#### Plans
- Planos de execução gerados pelo Planner Agent
- Planos de orquestração
- Planos de desenvolvimento
- Planos de deployment

#### Decisions
- Logs de decisões tomadas pelos Agents
- Justificativas de decisões
- Alternativas consideradas
- Consequências de decisões

#### Metrics
- Métricas de performance
- Métricas de qualidade
- Métricas de utilização
- Métricas de negócio

#### Summaries
- Sumarizações de documentos
- Sumarizações de execuções
- Sumarizações de análises
- Sumarizações de feedback

#### Insights
- Insights de análise de dados
- Insights de padrões
- Insights de anomalias
- Insights de oportunidades

#### Recommendations
- Recomendações de otimização
- Recomendações de melhoria
- Recomendações de arquitetura
- Recomendações de processo

### Como os Agents Utilizam

**Planner Agent**:
- Consulta `plans/` para planos anteriores
- Consulta `decisions/` para decisões passadas
- Consulta `metrics/` para estimativas

**Analytics Agent**:
- Consulta `analyses/` para análises anteriores
- Consulta `insights/` para insights gerados
- Consulta `metrics/` para métricas históricas

**Orchestrator Agent**:
- Consulta `reports/` para relatórios de execução
- Consulta `decisions/` para histórico de decisões
- Consulta `recommendations/` para melhorias

**Todos os Agents**:
- Consultam `summaries/` para contexto rápido
- Consultam `insights/` para aprendizado
- Consultam `recommendations/` para otimização

## Metadados das Fontes

Cada fonte de conhecimento possui metadados:

- **Tipo**: internal, external, generated
- **Categoria**: arquitetura, backend, frontend, etc.
- **Subcategoria**: subcategorias específicas
- **Versão**: versão do conhecimento
- **Atualização**: timestamp da última atualização
- **Acessibilidade**: agentes que podem acessar
- **Formato**: markdown, json, yaml, etc.
- **Tamanho**: tamanho do conhecimento
- **Popularidade**: frequência de acesso
- **Qualidade**: avaliação de qualidade

## Políticas de Acesso

### Internal Knowledge
- Acessível por todos os Agents
- Acesso em modo leitura
- Não modificável durante execução
- Versionado com o projeto

### External Knowledge
- Acessível por todos os Agents
- Acesso em modo leitura
- Pode referenciar recursos externos
- Atualizado periodicamente

### Generated Knowledge
- Acessível por todos os Agents
- Acesso em modo leitura/escrita
- Gerado dinamicamente
- Política de retenção aplicada
