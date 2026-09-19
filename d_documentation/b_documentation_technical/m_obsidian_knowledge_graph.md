# Grafo de Conhecimento Obsidian (Obsidian Knowledge Graph)

> **Documentação Técnica Oficial — Visualização Relacional Passiva e Navegação Humana**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[l_testing_strategy|Anterior: Estratégia de Testes]] | [[a_system_architecture|Início: Arquitetura do Sistema]]

---

## 1. O Papel do Obsidian: Camada de Visualização Humana

O workspace **Obsidian** configurado sob `.obsidian/` atua **exclusivamente como uma camada de visualização passiva e navegação semântica para seres humanos** (desenvolvedores, arquitetos e stakeholders).

### Princípio Arquitetural Inegociável:
> **"O Obsidian Graph NÃO é o SSOT e NÃO participa do runtime da fábrica."**

Os agentes de inteligência artificial da plataforma, o orquestrador (`MasterOrchestrator`) e o subsistema de execução leem diretamente os arquivos físicos em código (Python, YAML e Markdown) em `a_platform/c_brain/` e `a_platform/b_contracts/`. Nenhuma lógica de execução do AAF consulta metadados ou arquivos de configuração do Obsidian.

---

## 2. O que Entra e o que NÃO Entra no Grafo

Para manter o grafo do Obsidian limpo, semântico e focado em valor arquitetural:

| Categoria | Entra no Grafo Obsidian | NÃO Entra no Grafo Obsidian |
|---|---|---|
| **Conceitos de Engenharia** | Fases do Golden Path, Agentes nativos, catálogo de Skills, gates de auditoria, contratos e ciclo de reparo. | Logs transitórios de execução, arquivos temporários, diretórios de cache (`.pytest_cache`, `__pycache__`). |
| **Documentação** | Documentos canônicos estruturados em `d_documentation/a_documentation_functional/` e `d_documentation/b_documentation_technical/`. | Arquivos intermediários gerados em `e_generated_projects/` (cada projeto gerado é um artefato isolado). |
| **Regras e Políticas** | Regras arquiteturais e ADRs consolidadas no Brain (`a_platform/c_brain/b_rules/`). | Arquivos de estado de sessão JSON em `h_runtime/state/`. |
| **Conexões** | Relações causais reais representadas por wikilinks (`[[documento|Label]]`). | Links artificiais ou aleatórios criados apenas para inflar densidade de nós no grafo. |

---

## 3. Topologia Relacional do Grafo do Golden Path

O encadeamento semântico visualizado no Obsidian reflete a sequência real da engenharia:

```text
AAF (Visão Geral)
 │
 ├──► Discovery & Input
 │      ├──► Dataset Profiling
 │      └──► Brain (SSOT)
 │             ├──► Architecture
 │             └──► Planner
 │                    ├──► Tasks & Capabilities
 │                    └──► Skill Routing
 │                           ├──► Skill Index
 │                           ├──► Skill Registry (Lazy Loading)
 │                           └──► Multi-Skill Selection
 │
 ├──► Project Factory
 │      ├──► Agents Especialistas (DataAgent, DatabaseAgent, etc.)
 │      ├──► MCPs (Filesystem, Database, Docker)
 │      ├──► LLM Gateway (OpenAI Provider / gpt-4o-mini)
 │      └──► Artifacts (Memória)
 │
 ├──► Materializer (PathPolicy)
 │      └──► e_generated_projects/<project_id>/
 │
 └──► Runtime & Audit Gates
        ├──► Execution Runtime (CommandPolicy)
        ├──► Validation Gate
        ├──► Repair & Recovery Loop (Diagnóstico e Invalidação)
        ├──► Quality Engine (pytest, linters, bandit, pip check)
        ├──► Certification Engine (Conjunção Estrita)
        └──► PROJECT READY = YES
```

---

## 4. Rede de Navegação Semântica entre Documentos

A documentação do AAF utiliza links internos bidirecionais (`[[documento|Rótulo]]`) para permitir navegação em teia através do Obsidian:

1. **Jornada Funcional (`a_documentation_functional/`):**
   - [[a_aaf|Visão Geral do AAF]]
   - [[b_golden_path|Golden Path Oficial]]
   - [[c_discovery_and_input|Discovery e Entrada de Dados]]
   - [[d_planning_and_decomposition|Planejamento e Decomposição]]
   - [[e_agents_capabilities_and_skills|Agentes, Capabilities e Skills]]
   - [[f_project_generation|Geração e Fabricação de Projetos]]
   - [[g_execution_and_gates|Execução e Portões de Validação]]
   - [[h_repair_and_recovery|Reparo e Recuperação]]
   - [[i_project_ready_and_delivery|Project Ready e Entrega]]
   - [[j_operational_use|Uso Operacional da Plataforma]]
2. **Especificações Técnicas (`b_documentation_technical/`):**
   - [[a_system_architecture|Arquitetura do Sistema]]
   - [[b_contracts_and_state|Contratos e Gerenciamento de Estado]]
   - [[c_brain_and_context|Brain e Gestão de Contexto]]
   - [[d_planner_and_execution_plan|Planner e Plano de Execução]]
   - [[e_agents_and_skills|Agentes e Skills (Técnico)]]
   - [[f_mcps_and_llm_gateway|MCPs e LLM Gateway]]
   - [[g_factory_and_materialization|Fábrica e Materialização]]
   - [[h_runtime_and_command_policy|Runtime e Política de Comandos]]
   - [[i_validation_quality_certification|Validação, Qualidade e Certificação]]
   - [[j_repair_orchestration|Orquestração de Reparo]]
   - [[k_security_and_guardrails|Segurança e Guardrails]]
   - [[l_testing_strategy|Estratégia de Testes]]
   - [[m_obsidian_knowledge_graph|Grafo de Conhecimento Obsidian]]

---

## 5. Target Contract vs. Current Implementation Status

- **Target Contract:** O workspace `.obsidian/` possui visualizações em canvas e filtros por tags temáticas (`#core`, `#gate`, `#skill`, `#agent`) configuradas nativamente.
- **Current Implementation Status:** Os links canônicos `[[...]]` estão presentes em toda a documentação funcional e técnica, permitindo navegação relacional completa pelo Obsidian sem interferir no runtime do AAF.

---

## Navegação

- Documento anterior: [[l_testing_strategy|Estratégia de Testes]]
- Início da documentação técnica: [[a_system_architecture|Arquitetura do Sistema]]
- Início da documentação funcional: [[a_aaf|Visão Geral do AAF]]
