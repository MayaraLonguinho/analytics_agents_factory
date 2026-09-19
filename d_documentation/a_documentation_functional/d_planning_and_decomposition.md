# Planejamento e Decomposição Técnica

> **Documentação Funcional Oficial — Da Arquitetura ao Execution Plan**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[c_discovery_and_input|Anterior: Discovery e Input]] | [[e_agents_capabilities_and_skills|Próximo: Agentes, Capabilities e Skills]]

---

## 1. O Papel da Arquitetura (`ArchitectureDecision`)

Antes que qualquer linha de código ou tarefa de geração seja executada, o `ArchitectureAgent` (`a_platform/g_agents/c_architecture/`) realiza o enquadramento técnico da solução:

1. **Consulta às Regras do Brain:** Inspeciona as diretrizes arquiteturais em `a_platform/c_brain/b_rules/` para o domínio homologado;
2. **Seleção de Pilha Tecnológica:** Define formalmente:
   - Padrão arquitetural: **Modular Monolith** (obrigatório para projetos padrão AAF);
   - Linguagem base: Python (estruturado, tipado);
   - Persistência: SQLite / DuckDB local ou dialeto SQL analítico definido;
   - Suíte de validação: `pytest` para testes unitários automatizados;
3. **Emissão de `ArchitectureDecision`:** Documento estruturado contendo o framework de persistência, modelo analítico (ex: Star Schema ou Camadas Medallion), árvore de pastas recomendada e premissas de empacotamento.

---

## 2. A Entidade `ProjectPlan`

O `ProjectPlan` (`a_platform/b_contracts/f_plan.py`) é o documento normativo máximo emitido pelo `PlannerAgent` (`a_platform/g_agents/d_planner/`). Ele traduz a decisão de arquitetura em uma sequência determinística de tarefas atômicas e executáveis.

### 2.1 Estrutura Canônica do ProjectPlan
Um `ProjectPlan` válido contém obrigatoriamente:
- `project_id`: Identificador único da solicitação;
- `domain`: Domínio técnico validado (`analytics` ou `data_engineering`);
- `tasks`: Lista ordenada e tipada de `ProjectTask`;
- `run_commands`: Lista de comandos que o Runtime deve executar para validar e testar o projeto no disco;
- `expected_artifacts`: Lista de caminhos relativos de todos os arquivos físicos que devem existir ao final da geração.

---

## 3. Conceitos Fundamentais: Project, Task e Capability

A plataforma estabelece distinções inequívocas entre as camadas de decomposição:

```text
PROJECT (Objetivo Macro de Software)
  │
  ├── TASK 1 (Unidade de Trabalho Planejada)
  │     ├── Agente Designado (Responsabilidade)
  │     ├── Capabilities [1..N] (Necessidades Técnicas)
  │     ├── Depends On (Dependências com outras Tasks)
  │     ├── Expected Artifacts (Arquivos esperados)
  │     └── Validators (Critérios de aceitação)
  │
  ├── TASK 2 ...
  └── TASK N ...
```

- **Project:** O artefato completo e final entregue ao usuário (ex: "Pipeline ETL e Dashboard de Vendas com SQLite");
- **Task:** Uma unidade atômica de planejamento no DAG, associada a exatamente um agente responsável (ex: "Criar script de ingestão e limpeza de dados");
- **Capability:** A necessidade técnica explícita que a Task precisa suprir (ex: `data-cleaning`, `sql-analytics`, `data-quality`). Uma Task pode congregar múltiplas Capabilities quando a entrega exigir competências combinadas.

---

## 4. Dependências, Ordem e DAG de Tarefas

O `PlannerAgent` assegura que as tarefas formem um **Grafo Acíclico Dirigido (DAG)**:

1. **Resolução Topológica:** Nenhuma tarefa pode iniciar sua fabricação se as tarefas listadas em seu campo `depends_on` não tiverem sido previamente concluídas com seus artefatos devidamente registrados no contexto de geração;
2. **Prevenção de Ciclos:** Ciclos de dependência (ex: Tarefa A depende de B que depende de A) são sumariamente rejeitados na compilação do plano;
3. **Compartilhamento de Outputs:** Tarefas subsequentes herdam os metadados e os caminhos dos artefatos produzidos pelas tarefas precedentes (ex: a tarefa de modelagem SQL consome os nomes de tabelas definidos na tarefa de schema).

---

## 5. Atribuição de Agentes (`Agent Assignment`)

O Planner atribui cada tarefa a exatamente um agente especialista homologado:
- Tarefas de limpeza, profiling e ingestão de dados → `DataAgent`;
- Tarefas de schemas DDL, tabelas relacionais e queries → `DatabaseAgent`;
- Tarefas de agregações analíticas, KPIs e EDA → `AnalyticsAgent`;
- Tarefas de suíte de testes e validações de código → `TestingAgent`;
- Tarefas de README, guias de operação e documentação técnica → `DocumentationAgent`;
- Tarefas de API ou interface (quando requeridas) → `BackendAgent` ou `FrontendAgent`.

---

## 6. Preflight de Comandos e Validadores

O `PlannerAgent` não agenda comandos de forma ingênua:
1. **Preflight contra `CommandPolicy`:** Todos os `run_commands` associados às tarefas ou ao plano global passam por validação prévia contra a lista de binários homologados (`python`, `pytest`, etc.);
2. **Rejeição Antecipada:** Comandos inseguros, operadores de shell (`&&`, `|`, `;`) ou binários desconhecidos geram reprovação imediata do plano (`DENIED`), forçando o replanejamento antes que qualquer script seja executado;
3. **Injeção de Testes de Qualidade:** O Planner injeta compulsoriamente comandos de auditoria física de código (`pytest`, linters, verificação de dependências) para abastecer a futura fase de Quality.

---

## 7. Target Contract vs. Current Implementation Status

- **Target Contract:** O `PlannerAgent` recebe qualquer combinação de requisitos, resolve automaticamente o DAG de N tarefas, mapeia cada tarefa para suas capabilities correspondentes, seleciona agentes e compõe a suíte completa de validação sem intervenção humana.
- **Current Implementation Status:** O `PlannerAgent` implementa a decomposição em `ProjectPlan` com validação de domínios, preflight de `CommandPolicy` e injeção de comandos de teste. A estrutura de DAG e dependências entre tarefas opera serialmente garantindo ordem determinística de fabricação.

---

## Navegação

- Documento anterior: [[c_discovery_and_input|Discovery e Input]]
- Próximo passo funcional: [[e_agents_capabilities_and_skills|Agentes, Capabilities e Skills]]
- Referência técnica: [[d_planner_and_execution_plan|Planner e Plano de Execução]]
