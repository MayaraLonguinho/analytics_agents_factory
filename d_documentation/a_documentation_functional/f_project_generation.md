# Geração e Fabricação de Projetos

> **Documentação Funcional Oficial — Da Orquestração em Memória à Materialização em Disco**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[e_agents_capabilities_and_skills|Anterior: Agentes e Skills]] | [[g_execution_and_gates|Próximo: Execução e Portões de Validação]]

---

## 1. O Papel da Project Factory

A **Project Factory** (`a_platform/h_factory/a_project_factory.py`) é o motor de execução da esteira lógica de fabricação de software. Sua responsabilidade é processar o `ProjectPlan` emitido pelo Planner, coordenando os agentes especialistas e agregando as saídas em memória antes de qualquer escrita no disco.

A Factory atua como um maestro fabril:
1. Instancia dinamicamente os agentes necessários via `AgentFactory`;
2. Garante o isolamento entre tarefas;
3. Assegura que nenhum agente execute código fora do plano traçado;
4. Mantém a integridade do estado compartilhado durante todo o ciclo de vida.

---

## 2. O Contexto de Geração (`GenerationContext`)

Durante a fabricação, as tarefas operam sobre um contexto estruturado e seguro:
- **Histórico de Execução:** Registro de quais tarefas já foram concluídas com sucesso;
- **Herança de Dados:** Acesso aos outputs e metadados de tarefas anteriores (por exemplo, a tarefa de criação de pipeline precisa saber exatamente o nome do schema DDL gerado na tarefa de modelagem de banco);
- **Variáveis de Ambiente e Configuração:** Diretórios de trabalho, dialetos SQL adotados e políticas de segurança vigentes.

---

## 3. Execução Sequencial de Tarefas e Resolução de Dependências

A fábrica executa as tarefas seguindo a ordem determinada pelo DAG do plano:

```text
ProjectFactory
  │
  ├──► Task 1 (sem dependências) ──► Executa Agente/Skills ──► Registra Artifacts em Memória
  │
  ├──► Task 2 (depende de Task 1) ──► Consome Artifacts 1  ──► Executa Agente/Skills ──► Registra Artifacts
  │
  └──► Task N ...
```

- **Checagem Fail-Fast:** Se uma tarefa intermediária falhar na produção de seus artefatos obrigatórios (`expected_artifacts`), o pipeline é imediatamente pausado para acionar o diagnóstico de falha e o mecanismo de reparo, impedindo que tarefas subsequentes executem com premissas corrompidas.

---

## 4. O Conceito de Artifact (`Artifact Collection`)

Um **Artifact** (`a_platform/b_contracts/g_artifact.py`) é a representação lógica tipada de um arquivo gerado:
- **Atributos:**
  - `path`: Caminho relativo canônico dentro do projeto gerado (ex: `src/pipeline.py`, `sql/schema.sql`, `tests/test_etl.py`);
  - `type`: Tipo de conteúdo (`code`, `sql`, `config`, `doc`, `test`);
  - `content`: Conteúdo textual integral do arquivo em memória;
  - `producer`: Identificador do agente e skill responsáveis pela geração;
  - `metadata`: Metadados auxiliares de rastreabilidade.
- **Coleção de Artefatos:** Os artefatos residem estritamente em memória durante a fase de fábrica. Nenhum arquivo intermediário é gravado no disco antes da etapa oficial do Materializer.

---

## 5. O Materializer e a Proteção de Caminhos (`PathPolicy`)

O **ArtifactMaterializer** (`a_platform/i_materializer/a_materializer.py`) é a ponte mecânica e controlada entre os artefatos em memória e o sistema de arquivos físico.

### 5.1 Destino Exclusivo em Disco
Todos os projetos gerados pelo AAF são gravados obrigatoriamente dentro da árvore:
```text
e_generated_projects/<project_id>/
```

### 5.2 Segurança Rígida: PathPolicy
O Materializer aplica compulsoriamente a `PathPolicy` (`a_platform/i_materializer/b_path_policy.py`) em cada artefato:
- **Bloqueio de Path Traversal:** Rejeição imediata de caminhos contendo `..`, referências a diretórios superiores ou caracteres especiais maliciosos;
- **Bloqueio de Caminhos Absolutos:** Proibição de escrita fora do diretório raiz do projeto gerado (`/etc`, `/tmp`, raiz do repositório, etc.);
- **Isolamento Total:** Se qualquer artefato violar a política de caminhos, a materialização inteira é abortada com erro de segurança.

### 5.3 Persistência Atômica
- Criação dos subdiretórios necessários (`src/`, `sql/`, `tests/`, etc.);
- Gravação física com codificação UTF-8;
- Validação pós-escrita: conferência de que todos os arquivos declarados em `expected_artifacts` existem fisicamente no disco e possuem tamanho maior que zero bytes.

---

## 6. O Projeto Gerado (`e_generated_projects/<project_id>/`)

Ao término da materialização, o diretório gerado representa uma aplicação de software analítico independente, organizada como um Monolito Modular:
```text
e_generated_projects/<project_id>/
├── README.md               # Documentação técnica de execução
├── requirements.txt        # Dependências pinadas do projeto
├── sql/
│   └── schema.sql          # DDL e tabelas do projeto
├── src/
│   ├── ingestion.py        # Ingestão e tratamento
│   ├── pipeline.py         # Pipeline de dados e lógica analítica
│   └── analytics.py        # Consultas e métricas
├── tests/
│   └── test_pipeline.py    # Testes unitários automatizados (pytest)
└── data/                   # Diretório para bases de entrada e saída SQLite
```

---

## 7. Target Contract vs. Current Implementation Status

- **Target Contract:** A `ProjectFactory` consome o plano gerado pelo Planner, despacha para os agentes que acionam suas skills, recolhe os artefatos e os entrega ao `Materializer`, que persiste a estrutura com garantia de atomicidade e reversão transacional em caso de erro de I/O.
- **Current Implementation Status:** O fluxo `ProjectFactory` → `Artifact` → `ArtifactMaterializer` com aplicação de `PathPolicy` e escrita sob `e_generated_projects/<project_id>/` está plenamente implementado e funcional na plataforma.

---

## Navegação

- Documento anterior: [[e_agents_capabilities_and_skills|Agentes, Capabilities e Skills]]
- Próximo passo funcional: [[g_execution_and_gates|Execução e Portões de Validação]]
- Referência técnica: [[g_factory_and_materialization|Fábrica e Materialização (Técnico)]]
