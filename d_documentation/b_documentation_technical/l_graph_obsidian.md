# Grafo e Visualização no Obsidian

A documentação da Analytics Agents Factory foi estruturada para oferecer suporte nativo à navegação por grafos através do **Obsidian** (`.obsidian/`), permitindo visualização relacional das dependências, conceitos e fluxo da plataforma.

## Nova Estrutura Documental

A documentação em `d_documentation/` está estritamente organizada em duas categorias:

1. **`a_documentation_functional/` (Golden Path):**
   Conta a jornada cronológica de ponta a ponta na geração de um projeto, desde a requisição inicial até a prontidão:
   - `a_aaf.md` → `b_discovery.md` → `c_dataset_profiling.md` → `d_brain.md` → `e_architecture.md` → `f_planner.md` → `g_project_factory.md` → `h_agents.md` → `i_skills.md` → `j_mcps.md` → `k_llm_gateway.md` → `l_artifact.md` → `m_materializer.md` → `n_generated_projects.md` → `o_runtime.md` → `p_validation.md` → `q_repair_loop.md` → `r_quality.md` → `s_certification.md` → `t_project_ready.md`.

2. **`b_documentation_technical/` (Arquitetura e Implementação):**
   Explica a implementação, design modular e mecanismos internos em ordem lógica de abstração:
   - `a_architecture.md`: Estrutura de camadas do Modular Monolith.
   - `b_operation.md`: Modos de operação, CLI e máquinas de estado.
   - `c_brain.md`: Subsistema SSOT, regras e decisões.
   - `d_skills.md`: Subsistema de habilidades, catálogo e contratos.
   - `e_mcps.md`: Sandbox e protocolos operacionais (Filesystem, Database, Docker).
   - `f_agents.md`: Agentes nativos, fábrica e responsabilidades.
   - `g_llm_provider.md`: Gateway de IA e integração com provedor OpenAI.
   - `h_command_policy.md`: Preflight e enforcement de segurança em comandos.
   - `i_runtime.md`: Diferenciação entre Execution Runtime (`k_runtime`) e Session Runtime State (`h_runtime/state`).
   - `j_validation.md`: Validação funcional e ciclo de reparo automático.
   - `k_quality_certification.md`: Métricas de qualidade e motor de certificação.
   - `l_graph_obsidian.md`: Esta documentação de integração com o Obsidian Graph.
   - `m_presentation.md`: Roteiro de demonstração técnica para stakeholders.

## Grafo Conceitual do Golden Path

O grafo conceitual preserva o encadeamento visual no Obsidian:

```
AAF
 └── Discovery
      └── Dataset Profiling
           └── Brain
                └── Architecture
                     └── Planner
                          └── Project Factory
                               └── Agents
                                    └── Skills
                                         └── MCPs
                                              └── LLM Gateway
                                                   └── Artifact
                                                        └── Materializer
                                                             └── Generated Projects
                                                                  └── Runtime
                                                                       └── Validation
                                                                            ├── Repair Loop
                                                                            └── Quality
                                                                                 └── Certification
                                                                                      └── Project Ready
```

## O Graph NÃO é o SSOT

- **Aviso Arquitetural:** O Obsidian Graph é exclusivamente uma ferramenta de **visualização passiva** para desenvolvedores e arquitetos.
- O código da plataforma, os agentes e o `MasterOrchestrator` não consomem metadados do Obsidian em tempo de execução. O conhecimento de negócio e as regras residem incondicionalmente nos arquivos físicos de `a_platform/c_brain/` (Single Source of Truth).
