# Arquitetura do Sistema (System Architecture)

> **Documentação Técnica Oficial — Topologia, Limites e Padrões Estruturais**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[b_contracts_and_state|Próximo: Contratos e Gerenciamento de Estado]]

---

## 1. Padrão Arquitetural: Modular Monolith

O **Analytics Agents Factory (AAF)** é formalmente concebido e implementado como um **Monolito Modular** (Modular Monolith). Esta decisão de engenharia é estratégica e deliberada:

1. **Simplicidade Operacional:** Elimina a complexidade de redes distribuídas, RPCs, orquestração de microsserviços e mensageria assíncrona externa na fase de desenvolvimento e operação padrão;
2. **Forte Coesão e Baixo Acoplamento:** O sistema é estruturado em módulos independentes com responsabilidades rigorosamente delimitadas, comunicando-se exclusivamente por meio de contratos de dados fortemente tipados (`a_platform/b_contracts/`);
3. **Determinismo e Rastreabilidade:** Permite a execução sequencial controlada do Golden Path, facilitando auditoria, profiling de performance e depuração ponta a ponta;
4. **Isolamento de Efeitos Colaterais:** Cada módulo possui fronteiras públicas bem definidas, impedindo que alterações internas vazem para outras camadas da plataforma.

---

## 2. Árvore Estrutural Oficial de Referência

A topologia do repositório AAF reflete a ordenação lógica e a separação de responsabilidades:

```text
analytics_agents_factory/
├── .agents/                        # Contrato normativo da IDE (a_AGENT.md)
├── .obsidian/                      # Configuração do espaço de visualização humana
│
├── a_platform/                     # Núcleo funcional da fábrica
│   ├── b_contracts/                # Modelos Pydantic, DTOs e StateManager
│   ├── c_brain/                    # SSOT de conhecimento, regras, domínios e decisões
│   ├── e_skills/                   # Catálogo, índice, roteador e implementação de Skills
│   ├── f_mcps/                     # Protocolos seguros de I/O (Filesystem, Database, Docker)
│   ├── g_agents/                   # Agentes de orquestração e agentes especialistas
│   ├── h_factory/                  # Orquestrador lógico de fabricação (ProjectFactory)
│   ├── i_materializer/             # Persistência física de arquivos e PathPolicy
│   ├── j_llm_gateway/              # Abstração de provedores de IA e roteamento de modelos
│   ├── k_runtime/                  # Execution Runtime seguro e CommandPolicy
│   ├── l_validation/               # Gates de validação estrutural, de sintaxe e execução
│   ├── m_quality/                  # Motor de avaliação de testes, linters e dependências
│   ├── n_certification/            # Motor de auditoria final e concessão de prontidão
│   └── o_orchestration/            # Orquestrador mestre (MasterOrchestrator e RepairLoop)
│
├── b_input/                        # Diretório de entrada para datasets de usuários
├── c_tests/                        # Suíte de testes da própria plataforma AAF
├── d_documentation/                # Documentação técnica e funcional canônica
│   ├── a_documentation_functional/ # Jornada do usuário e comportamento funcional
│   └── b_documentation_technical/  # Especificações arquiteturais e de implementação
│
├── e_generated_projects/           # Diretório isolado para gravação dos projetos gerados
├── f_cli/                          # Interface de linha de comando oficial (aaf)
├── g_configuration/                # Configurações globais e carregamento de settings
└── h_runtime/                      # Estado persistente de sessão
    └── state/                      # Checkpoints JSON (<project_id>.json)
```

---

## 3. Limites de Camadas (Boundaries) e Regras de Acoplamento

A integridade do Monolito Modular é protegida por regras rígidas de dependência:

1. **Unidirecionalidade das Dependências:**  
   Módulos inferiores não conhecem módulos superiores. Por exemplo, `b_contracts` e `c_brain` nunca importam de `g_agents` ou `o_orchestration`.
2. **Abstração Obrigatória de LLM:**  
   Nenhum agente, skill ou contrato importa diretamente SDKs de provedores externos (`openai`, `anthropic`, `google.generativeai`). Todo acesso a modelos é mediado exclusivamente por `a_platform/j_llm_gateway/`.
3. **Acesso Físico Restrito a MCPs:**  
   Agentes e skills não executam `os.system`, `subprocess` aberto ou I/O direto para manipular banco ou arquivos do projeto gerado. Toda operação física é despachada via `a_platform/f_mcps/`.
4. **Isolamento do Workspace de Projetos:**  
   A gravação de arquivos gerados é matematicamente restrita a `e_generated_projects/<project_id>/` via `PathPolicy`. Qualquer tentativa de escrita externa gera bloqueio imediato.
5. **Diferenciação Estrita de Runtimes:**
   - `a_platform/k_runtime/`: **Execution Runtime** — executa os comandos dos projetos gerados em subprocesso seguro;
   - `h_runtime/state/`: **Session Runtime State** — armazena checkpoints JSON do ciclo de vida da plataforma.

---

## 4. Fluxo Sequencial de Dependência do Golden Path

O fluxo de dados entre os componentes da plataforma obedece à sequência linear:

```text
ProjectRequest (CLI / Adapter)
       ↓
DiscoveryAgent (Elicitação e validação de requisitos)
       ↓
DatasetProfilingSkill (Inspeção física factual de dados)
       ↓
Brain (Consolidação de regras de domínio e arquitetura)
       ↓
ArchitectureAgent (Seleção de stack e patterns)
       ↓
PlannerAgent (Decomposição em DAG de Tasks e Capabilities)
       ↓
SkillRouter (Roteamento multi-skill, deduplicação e dependências)
       ↓
ProjectFactory (Orquestração de agentes e emissão de Artifacts em memória)
       ↓
ArtifactMaterializer (Persistência física sob PathPolicy)
       ↓
ProjectRuntime (Execução real de comandos sob CommandPolicy)
       ↓
ValidationGate (Auditoria de sintaxe, arquivos e exit codes)
       ↓
QualityEngine (Auditoria de testes pytest, linters e dependências)
       ↓
CertificationEngine (Laudo de prontidão final)
       ↓
PROJECT READY = YES
```

---

## 5. Target Contract vs. Current Implementation Status

- **Target Contract:** O Monolito Modular possui limites rígidos com verificação automática de acoplamento por ferramentas de linting arquitetural, garantindo que novos módulos não introduzam dependências circulares.
- **Current Implementation Status:** A estrutura de diretórios, separação por camadas alfabéticas em `a_platform/`, isolamento do LLM Gateway e centralização de contratos em `b_contracts/` estão consolidadas no código.

---

## Navegação

- Documento anterior (Funcional): [[j_operational_use|Uso Operacional]]
- Próximo passo técnico: [[b_contracts_and_state|Contratos e Gerenciamento de Estado]]
- Grafo de conhecimento: [[m_obsidian_knowledge_graph|Grafo Obsidian]]
