# Brain e Gestão de Contexto (Brain & Context)

> **Documentação Técnica Oficial — Subsistema SSOT de Conhecimento e Políticas**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[b_contracts_and_state|Anterior: Contratos e Estado]] | [[d_planner_and_execution_plan|Próximo: Planner e Plano de Execução]]

---

## 1. O Conceito de Brain como SSOT

O **Brain** (`a_platform/c_brain/`) é a **Fonte Única da Verdade (Single Source of Truth — SSOT)** de contexto operacional, políticas arquiteturais e conhecimento normativo do Analytics Agents Factory.

Durante a fabricação de um projeto analítico, agentes de IA não tomam decisões com base em opiniões probabilísticas soltas; eles consultam o Brain para recuperar regras de design, diretrizes de modelagem de dados, padrões de queries SQL e guardrails homologados.

---

## 2. Estrutura Interna e Organização de Diretórios

O Brain é estruturado em subpastas com responsabilidades conceituais estritas:

```text
a_platform/c_brain/
├── a_context/          # Definições de baseline, escopo analítico e metadados operacionais
├── b_rules/            # Regras normativas de engenharia e conformidade
│   ├── c_architecture_rules.md   # Modular Monolith, padrões de empacotamento
│   ├── d_data_rules.md           # Convenções de nomenclatura, tipagem e integridade
│   ├── e_sql_rules.md            # Dialetos SQL permitidos, uso de CTEs, sanitização
│   ├── f_testing_rules.md        # Diretrizes para suítes pytest obrigatórias
│   ├── g_documentation_rules.md  # Padrões para README.md e manifestos técnicos
│   └── h_project_ready_rules.md  # Critérios de concessão do selo PROJECT READY
├── c_patterns/         # Catálogo de padrões de código (ETL, queries analíticas, Dockerfile)
├── d_domains/          # Especializações por domínio técnico e guardrails
│   ├── a_analytics.md            # Configurações do domínio Analytics
│   ├── b_data_engineering.md     # Configurações do domínio Data Engineering
│   └── b_domains.yaml            # Declaração canônica de domínios e allowed_skills
├── e_decisions/        # Registro formal de decisões arquiteturais (ADRs históricas)
├── f_graph/            # Relações semânticas e topológicas entre conceitos do sistema
├── g_brain.py          # Fachada principal do Brain (Brain API)
└── h_learning_engine.py# Motor experimental de aprendizado (fora do Golden Path)
```

---

## 3. Gestão Progressiva de Contexto (`Progressive Context`)

O Brain implementa a técnica de **injeção progressiva de contexto**:
1. **Evita Saturação do Prompt:** Não despeja todas as regras no prompt de todos os agentes. Um agente de documentação recebe apenas `g_documentation_rules.md`, enquanto o `DatabaseAgent` recebe `e_sql_rules.md` e `d_data_rules.md`;
2. **Contexto por Fase:** O `ArchitectureAgent` consome o contexto de requisitos e perfil de dados para filtrar apenas os padrões relevantes ao domínio (`c_patterns/`);
3. **Eficiência e Custo:** Reduz drasticamente o consumo de tokens e foca a atenção do modelo exclusivamente nas restrições pertinentes à tarefa ativa.

---

## 4. Distinção Obrigatória: Brain vs. Obsidian Graph

Uma das regras fundamentais da arquitetura do AAF é a separação irrevogável entre lógica e visualização:

| Atributo | Brain (`a_platform/c_brain/`) | Obsidian (`.obsidian/` e links markdown) |
|---|---|---|
| **Papel** | **SSOT Operacional em Código.** Motor que alimenta agentes, orquestrador e decisões da plataforma. | **Camada de Visualização Humana.** Ferramenta passiva para leitura e navegação em grafo por pessoas. |
| **Execução** | Lido e processado programaticamente por classes Python (`g_brain.py`). | Não possui código executável; não participa do runtime da fábrica. |
| **Autoridade** | Se houver conflito, o Brain é a verdade canônica. | O Obsidian apenas reflete passivamente o que existe no repositório. |

**Alerta Normativo:** O Obsidian **NÃO substitui o Brain**. Agentes de desenvolvimento e desenvolvedores jamais devem depender de plugins ou metadados do Obsidian para controlar a lógica da fábrica.

---

## 5. Status do Learning Engine (`h_learning_engine.py`)

O módulo `h_learning_engine.py` é um componente experimental voltado para futuras rotinas de aprendizado pós-execução e **encontra-se formalmente fora do Golden Path oficial**. 
O pipeline principal do AAF não executa, não consome e não depende do Learning Engine para conduzir a fabricação nem para conceder o status `PROJECT READY = YES`.

---

## 6. Target Contract vs. Current Implementation Status

- **Target Contract:** O Brain atua como um sistema de RAG semântico híbrido local, indexando regras por embeddings vetoriais locais e recuperando trechos normativos específicos sob demanda de cada prompt.
- **Current Implementation Status:** A fachada `g_brain.py` e os registros de regras (`RuleRegistry`, `DomainRegistry`, `PatternRegistry`) estão consolidados em código, lendo os arquivos markdown e YAML em `a_platform/c_brain/` e injetando o contexto estruturado no `ExecutionContext`.

---

## Navegação

- Documento anterior: [[b_contracts_and_state|Contratos e Estado]]
- Próximo passo técnico: [[d_planner_and_execution_plan|Planner e Plano de Execução]]
- Referência visual: [[m_obsidian_knowledge_graph|Grafo de Conhecimento Obsidian]]
