# Fábrica e Materialização (Factory & Materialization)

> **Documentação Técnica Oficial — Orquestração de Código em Memória e Persistência Física**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[f_mcps_and_llm_gateway|Anterior: MCPs e LLM Gateway]] | [[h_runtime_and_command_policy|Próximo: Runtime e Política de Comandos]]

---

## 1. O Pipeline de Fabricação Lógica

A fabricação de um projeto no AAF é dividida em duas etapas rigorosamente isoladas:

```text
[ ProjectPlan ]
       │
       ▼
1. ETAPA EM MEMÓRIA: ProjectFactory
   - Itera sobre as tarefas do DAG
   - Despacha para os Agentes Especialistas
   - Executa Skills roteadas
   - Coleta instâncias tipadas de Artifact
       │
       ▼
2. ETAPA EM DISCO: ArtifactMaterializer
   - Aplica a PathPolicy (Sandbox)
   - Valida colisões de escrita
   - Grava fisicamente em e_generated_projects/<project_id>/
```

Essa separação impede que falhas parciais de agentes deixem arquivos órfãos ou quebrados no sistema de arquivos físico.

---

## 2. A Arquitetura da `ProjectFactory` (`a_platform/h_factory/`)

Implementada em `a_platform/h_factory/a_project_factory.py`, a classe `ProjectFactory` é o orquestrador do ciclo fabril:

### 2.1 O Contexto de Geração (`GenerationContext`)
Objeto de estado que acompanha a execução das tarefas:
- Armazena a lista de artefatos acumulados até o momento;
- Fornece às tarefas correntes os artefatos produzidos pelas tarefas anteriores (ex: scripts SQL gerados pela Tarefa 1 são disponibilizados no contexto da Tarefa 2);
- Registra métricas de tempo e contagem de artefatos.

### 2.2 Despacho de Tarefas e Coleta (`ArtifactCollector`)
1. Para cada tarefa no DAG:
   - Obtém a instância do agente na `AgentFactory`;
   - Invoca o agente passando a `ProjectTask` e o `GenerationContext`;
   - O agente aciona as habilidades via `SkillRegistry` e gera o código correspondente;
   - Os artefatos retornados são validados sintaticamente e adicionados à coleção do projeto;
2. Se uma tarefa falhar ou não emitir todos os seus `expected_artifacts`, a Factory aborta o ciclo imediatamente (*fail-fast*).

---

## 3. A Arquitetura do `Materializer` (`a_platform/i_materializer/`)

O **ArtifactMaterializer** (`a_materializer.py`) é o executor mecânico responsável por converter a lista de `Artifact[]` em arquivos reais no disco.

### 3.1 Segurança de Disco e `PathPolicy` (`b_path_policy.py`)
Antes de criar qualquer arquivo, cada caminho relativo do artefato é submetido à `PathPolicy`:
- **Resolução Canônica:** O caminho relativo é resolvido contra o diretório base:
  ```python
  target_full_path = os.path.realpath(os.path.join(project_base_dir, artifact.path))
  ```
- **Asserção de Prefixo:** O `target_full_path` deve obrigatoriamente iniciar com `project_base_dir`;
- **Rejeição de Traversal:** Qualquer uso de `..`, links simbólicos maliciosos ou caracteres nulos resulta em `PathPolicyViolationError`, bloqueando a gravação;
- **Destino Obrigatório:** O diretório base é invariavelmente restrito a:
  ```text
  e_generated_projects/<project_id>/
  ```

### 3.2 O Escritor de Artefatos (`ArtifactWriter` em `c_artifact_writer.py`)
- Cria os diretórios pai recursivamente (`os.makedirs(exist_ok=True)`);
- Persiste o conteúdo textual com encoding explícito UTF-8;
- Aplica permissões de arquivo adequadas (ex: permissão de execução para scripts shell, quando aplicável);
- Validação pós-escrita: confere existência física e tamanho em bytes para atestar que o disco persistiu o conteúdo com integridade.

---

## 4. O Projeto de Saída (`Output Project`)

Ao final do ciclo do Materializer, o diretório gerado está estruturado e pronto para execução pelo Runtime:

```text
e_generated_projects/<project_id>/
├── README.md               # Instruções de execução e documentação
├── requirements.txt        # Dependências pinadas do projeto
├── sql/
│   └── schema.sql          # DDL analítico e tabelas
├── src/
│   ├── ingestion.py        # Módulo de ingestão e sanitização
│   ├── pipeline.py         # Pipeline de transformação e cálculo
│   └── analytics.py        # Queries e relatórios analíticos
├── tests/
│   └── test_pipeline.py    # Testes unitários com pytest
└── data/                   # Diretório reservado para banco de dados local SQLite
```

O Materializer emite o objeto `MaterializationResult(status="PASSED", materialized_paths=[...])`, liberando o avanço para a fase de Runtime.

---

## 5. Target Contract vs. Current Implementation Status

- **Target Contract:** O Materializer opera com transacionalidade total (duas fases: gravação em staging temporário e atomic rename do diretório final), garantindo que em caso de interrupção abrupta de energia ou I/O, o diretório antigo não seja corrompido.
- **Current Implementation Status:** O `ProjectFactory`, o `ArtifactMaterializer`, a `PathPolicy` e o `ArtifactWriter` estão implementados e operacionais, gravando com sucesso os artefatos gerados em `e_generated_projects/<project_id>/`.

---

## Navegação

- Documento anterior: [[f_mcps_and_llm_gateway|MCPs e LLM Gateway]]
- Próximo passo técnico: [[h_runtime_and_command_policy|Runtime e Política de Comandos]]
- Visão funcional: [[f_project_generation|Geração de Projetos (Funcional)]]
