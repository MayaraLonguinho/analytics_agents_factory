# Analytics Agents Factory — IDE Agent Contract

> **Documento Normativo Oficial — Constituição Operacional e Arquitetural do AAF**  
> **Status:** Ativo / Mandatório para qualquer IDE Agent, AI Coding Agent ou Desenvolvedor.  
> **Escopo de Aplicação:** Governança, desenvolvimento, refatoração, manutenção e operação do ecossistema Analytics Agents Factory (AAF).

---

## 1. Identidade

O **Analytics Agents Factory (AAF)** é uma plataforma multiagente determinística e modular projetada para a fabricação automatizada de projetos de software completos, executáveis e certificados no espaço de dados. O AAF opera como um **Monolito Modular** de alta coesão e baixo acoplamento, regido por contratos estritos de dados, barramentos controlados de execução e gates formais de validação.

No desenvolvimento e manutenção desta plataforma, qualquer agente de inteligência artificial ou desenvolvedor humano deve assumir a postura de **Principal Software Architect & AI Systems Architect**, zelando pela conformidade arquitetural, integridade conceitual e fidelidade estrita às regras aqui consagradas.

---

## 2. Missão

A missão do AAF é transformar solicitações de usuários em linguagem natural — combinadas ou não com datasets brutos — em projetos analíticos estruturados, materializados em disco, efetivamente executados em ambiente de runtime, rigorosamente testados, validados contra contratos técnicos e formalmente certificados para entrega, sem intervenção manual de código e sem atalhos que comprometam a qualidade de engenharia.

---

## 3. Escopo Técnico

O AAF é especializado tecnicamente e de forma estrita nas seguintes disciplinas:

1. **Data Engineering:** Ingestão de dados estruturados e semiestruturados, pipelines de ETL/ELT determinísticos, orquestração de fluxos de transformação, observabilidade e linhagem de pipelines;
2. **Analytics Engineering:** Modelagem dimensional (Star Schema, Snowflake, tabelas fato e dimensões), modelagem em camadas modulares (raw, staging, intermediate, marts), views e agregações analíticas;
3. **Analytics & Data Analysis:** Análise exploratória de dados (EDA), estatística descritiva, correlações, distribuição de variáveis, cálculo e agregação de KPIs e métricas de negócio, geração de visualizações e relatórios estruturados;
4. **Machine Learning Básica/Analítica (quando aplicável):** Engenharia e seleção de features, treinamento supervisionado basilar, avaliação e inferência em lote;
5. **SQL Analítico & Otimização:** Dialetos compatíveis com bancos relacionais e analíticos (PostgreSQL, DuckDB, SQLite), CTEs, window functions, planos de execução e indexação analítica;
6. **Qualidade & Validação de Dados:** Asserções de integridade, completude, consistência, testes de schema, profiling e validação sintática/semântica;
7. **Documentação Técnica Automatizada:** Especificações arquiteturais, dicionários de dados, linhagem e guias operacionais de execução (README, manuais de reprodução).

---

## 4. Fora de Escopo

Estão expressamente **fora de escopo** do AAF, devendo ser sumariamente rejeitados ou não implementados pela plataforma:

1. **Regras de Negócio Arbitrárias ou Inventadas:** O AAF é rigorosamente **agnóstico ao domínio de negócio** (atende vendas, finanças, saúde, RH, logística, marketing, etc., sem preconceber premissas de negócio não declaradas pelo usuário);
2. **Sistemas Web Full-Stack Genéricos:** O AAF não é um gerador de e-commerce, blogs, CRMs transacionais (OLTP puro) ou portais sociais;
3. **Microserviços Distribuídos como Padrão:** Não criar arquiteturas orientadas a microserviços no core da plataforma ou nos projetos padrão (o padrão absoluto é Modular Monolith);
4. **Alucinação de Fontes e Destinos Críticos:** É vedado inventar conexões a bancos de produção, credenciais fictícias ou repositórios remotos sem declaração do usuário;
5. **Geração Cosmética de Código:** Projetos que apenas compilam mas não possuem lógica analítica executável, pipelines vazios ou meros placeholders (`pass`, `TODO`, mocks permanentes).

---

## 5. Contrato Funcional Oficial

O Contrato Funcional Oficial do AAF é a definição normativa máxima que rege todo o ciclo de vida do sistema:

> *"O AAF recebe uma solicitação em linguagem natural, descobre e estrutura os requisitos, analisa os dados disponíveis quando aplicável, consolida o contexto no Brain, define a arquitetura, cria um ProjectPlan, decompõe o projeto em Tasks e Capabilities, atribui os Agents responsáveis, seleciona as Skills necessárias, estabelece a ordem e as dependências de execução, gera os Artifacts, materializa o projeto, executa o projeto realmente gerado e o conduz sequencialmente pelos gates de Validation, Quality e Certification. Quando uma falha recuperável ocorre, o AAF diagnostica a causa raiz, identifica a fase responsável, invalida os resultados posteriores afetados, retorna à fase responsável, corrige e reprocessa o fluxo. Quando uma decisão indispensável depende do usuário, o AAF entra em NEEDS_INPUT/PAUSED e continua após a resposta. O encerramento normal da fabricação ocorre somente quando todos os critérios de prontidão forem satisfeitos e PROJECT READY = YES, quando então o projeto funcional é entregue ao usuário."*

Essa definição é inegociável e não pode ser relaxada ou enfraquecida por nenhuma implementação ou intervenção.

---

## 6. Golden Path Oficial

O fluxo operacional e sequencial de fabricação do AAF segue estritamente a árvore abaixo:

```text
USER REQUEST
    ↓
IDE Chat / CLI
    ↓
DISCOVERY
    ↓
[NEEDS_INPUT?]
    ├── SIM → PAUSED → USER ANSWER → RESUME → DISCOVERY
    └── NÃO
          ↓
DATASET PROFILING (quando aplicável)
    ↓
BRAIN (consolidação de contexto, domínios, regras e evidências)
    ↓
ARCHITECTURE (definição de stack, padrões e guardrails)
    ↓
PLANNER (decomposição técnica)
    ↓
PROJECT PLAN
    ↓
PROJECT → TASKS [1..N]
    ↓
CAPABILITIES [1..N]
    ↓
AGENT ASSIGNMENT
    ↓
SKILL ROUTING (SkillRouter determinístico)
    ↓
SKILL INDEX (SkillIndex catalogado)
    ↓
DOMAIN / AGENT GUARDRAILS (allowed_skills / allowed_agents)
    ↓
SKILLS [1..N] (resolução multi-skill e ordenação por dependências)
    ↓
EXECUTION PLAN
    ↓
PROJECT FACTORY
    ↓
TASK 1 ──→ AGENT ──→ SKILLS NECESSÁRIAS (SkillRegistry) ──→ BRAIN/MCPs/LLM GATEWAY ──→ ARTIFACTS
    ↓
TASK 2 ──→ AGENT ──→ SKILLS NECESSÁRIAS (SkillRegistry) ──→ BRAIN/MCPs/LLM GATEWAY ──→ ARTIFACTS
    ↓
...
    ↓
TASK N ──→ ARTIFACTS
    ↓
MATERIALIZER
    ↓
e_generated_projects/<project_id>/
    ↓
RUNTIME (execução real dos artefatos em ambiente isolado)
    ↓
VALIDATION (validação de outputs, schemas, exit codes e arquivos)
    ↓
QUALITY (avaliação de asserções, cobertura, linters e dependências)
    ↓
CERTIFICATION (verificação holística de conformidade e prontidão)
    ↓
PROJECT READY = YES
    ↓
RESULT
    ↓
PROJETO ENTREGUE AO USUÁRIO
```

**Restrição de Sequência Canônica:**  
`Context → Plan → Decisions → Skills → Execution → Materialization → Gates`

---

## 7. Estados Operacionais

A máquina de estados oficial do AAF (`StateManager`) reconhece formalmente os seguintes estados do ciclo de vida:

| Estado | Descrição |
|---|---|
| `INITIALIZED` | Projeto criado no sistema com `project_id` gerado e contexto instanciado. |
| `DISCOVERY` | Fase de elicitação e levantamento de requisitos em execução. |
| `NEEDS_INPUT` | Fase de bloqueio ativo aguardando informação indispensável do usuário. |
| `PAUSED` | Sessão temporariamente suspensa aguardando interação externa na CLI/IDE. |
| `RESUMED` | Sessão reativada após recebimento de resposta do usuário; retoma na fase de origem. |
| `PROFILING` | Execução técnica de análise e caracterização de dataset fornecido. |
| `ARCHITECTING` | Elaboração da arquitetura técnica, seleção de patterns e contratos. |
| `PLANNING` | Decomposição do projeto em `ProjectPlan`, `Tasks`, `Capabilities` e `Skills`. |
| `GENERATING` | `ProjectFactory` orquestrando agentes e skills para emitir `Artifacts`. |
| `MATERIALIZING` | Gravação física dos arquivos em `e_generated_projects/<project_id>/`. |
| `EXECUTING` | `Runtime` executando scripts, comandos e testes do projeto gerado. |
| `VALIDATING` | Avaliação de contratos estruturais e funcionais no `ValidationGate`. |
| `REPAIRING` | Ciclo de correção ativo: diagnóstico, invalidação a jusante e reprocessamento. |
| `QUALITY_CHECK` | Avaliação das métricas e evidências de qualidade pelo `QualityEngine`. |
| `CERTIFYING` | Auditoria final de todos os critérios de aceite pelo `CertificationEngine`. |
| `READY` | Conclusão bem-sucedida: todos os gates aprovados (`PROJECT READY = YES`). |
| `FAILED` | Estado terminal anômalo após esgotamento definitivo de reparos não recuperáveis. |

---

## 8. Discovery Protocol

O `DiscoveryAgent` é o componente encarregado da elucidação dos requisitos. Suas regras operacionais são estritas:

1. **Limite Estrito de Perguntas:** No **máximo 5 perguntas** em toda a sessão de Discovery;
2. **Sequencialidade:** Exatamente **uma pergunta por vez** (`one question at a time`);
3. **Critério de Relevância:** Apenas perguntar quando a resposta puder alterar decisivamente:
   - Arquitetura técnica;
   - Escopo do projeto;
   - Capability requerida;
   - Fonte de dados (`source`) ou destino analítico (`target`);
   - Critério de aceite ou validação;
   - Decisão técnica indispensável;
4. **Assumptions Explícitas:** Incertezas menores, detalhes cosméticos ou parâmetros secundários **não** devem motivar perguntas; devem ser convertidos em **premissas técnicas explícitas (`assumptions`)** e registradas no Brain;
5. **Decisões Não Resolvidas (Q-NN):** Dúvidas dependentes de confirmação futura devem ser estruturadas sob identificadores canônicos `Q-01`, `Q-02`, etc.;
6. **Não Inventar Regras:** Jamais presumir regras de negócio do cliente ou inventar infraestruturas inexistentes;
7. **Bloqueio por Falta de Dado Crítico:** Se uma informação for imprescindível para avançar, transitar imediatamente para `NEEDS_INPUT → PAUSED`;
8. **Retomada:** Recebida a resposta, transitar para `RESUME` e retornar à fase adequada do Discovery.

---

## 9. Dataset Profiling

Quando o usuário fornece um dataset (ou aponta um caminho em `b_input/`), o `DatasetProfilingSkill` entra em ação antes das fases de Arquitetura e Planejamento:

1. **Evidência Real:** Utiliza Pandas/DuckDB para inspecionar os dados reais, coletando:
   - Volume de linhas e colunas;
   - Nomes literais e tipos inferidos de colunas;
   - Cardinalidade, percentual de nulos e registros duplicados;
   - Anomalias de formatação, caracteres corrompidos e outliers preliminares;
2. **Alimentação do Brain:** Os metadados apurados são consolidados no Brain sob a categoria `evidence`;
3. **Aderência:** O `ArchitectureAgent` e o `PlannerAgent` utilizam as evidências do profiling para determinar o schema de tabelas, estratégias de limpeza (`data-cleaning`) e modelos dimensionais;
4. **Proibição:** É proibido presumir colunas ou tipos fictícios quando um arquivo de dados real estiver disponível.

---

## 10. Brain

O **Brain** é a Fonte Única da Verdade (Single Source of Truth — SSOT) de conhecimento e contexto operacional da plataforma AAF durante a fabricação de um projeto.

1. **Estrutura Conceitual do Brain:**
   - `context`: Identificador de projeto, objetivos declarados, premissas (`assumptions`) e estado corrente;
   - `requirements`: Requisitos funcionais e técnicos validados no Discovery;
   - `evidence`: Evidências concretas (resultados de profiling, outputs de execução, métricas de dados);
   - `rules`: Regras arquiteturais, guardrails de domínio e restrições de engenharia;
   - `patterns`: Padrões de projeto homologados (ex: Star Schema, ETL procedural, camadas Medallion);
   - `domains`: Domínios configurados (`b_domains.yaml`), skills permitidas e templates aplicáveis;
   - `decisions`: Registro formal de decisões arquiteturais (ADRs, trade-offs e resoluções `Q-NN`);
   - `graph`: Relações topológicas entre entidades, conceitos e tarefas do projeto.
2. **Distinção Mandatória — Brain vs. Obsidian:**
   - O **Brain** (`a_platform/c_brain/`) é a estrutura de dados operacional em código (Python/YAML) consumida ativamente pelos agentes e orquestradores.
   - O **Obsidian** (`.obsidian/` e links markdown em `d_documentation/`) é **exclusivamente uma interface humana de visualização**, navegação e documentação estática.
   - O Obsidian **NÃO** executa lógica, **NÃO** decide regras e **NÃO** substitui o Brain.

---

## 11. Architecture

O `ArchitectureAgent` é o único agente responsável por estabelecer a base técnica do projeto a ser gerado:

1. **Entradas:** Requisitos consolidados no Brain, evidências de profiling e guardrails do domínio;
2. **Saídas:** Stack tecnológica selecionada, estrutura de diretórios do projeto gerado, convenções de código, dialeto SQL e padrões de modelagem analítica;
3. **Modular Monolith Obrigatório:** O projeto gerado deve ser concebido como um monolito modular autocontido, garantindo simplicidade de empacotamento, reprodutibilidade e ausência de dependências de rede externas complexas;
4. **Proibição de Desvios:** É proibido introduzir frameworks não catalogados ou criar microserviços sem solicitação explícita fundamentada em ADR arquivada no Brain.

---

## 12. Planning

O `PlannerAgent` traduz a arquitetura em um plano operacional rigoroso (`ProjectPlan`):

1. **Decomposição Determinística:** Decompõe o objetivo global em `Tasks` sequenciais ou organizadas em DAG (Directed Acyclic Graph);
2. **Associação Explícita:** Para cada tarefa, o Planner define:
   - Descrição objetiva da entrega;
   - Agente especialista designado para a execução;
   - Capabilities necessárias (1..N);
   - Skills necessárias requeridas via catálogo;
   - MCPs operacionais exigidos;
   - Dependências diretas em relação a tarefas anteriores (`depends_on`);
   - Comandos de validação e critérios de aceitação específicos;
3. **Validação do Plano:** O `ProjectPlan` deve ser estruturado conforme o contrato `a_platform/b_contracts/f_plan.py`.

---

## 13. Project / Task / Capability

A hierarquia formal e a cardinalidade entre as entidades de trabalho do AAF são imutáveis:

```text
1 Project ───► 1..N Tasks
1 Task    ───► 1..N Capabilities
1 Task    ───► 1 Agente Responsável
1 Task    ───► 1..N Skills (quando a tarefa demandar múltiplas competências)
```

- **Project:** Unidade macro solicitada pelo usuário, encapsulando todo o ciclo de vida, artefatos e gates;
- **Task:** Unidade elementar de planejamento e execução dentro do `ProjectPlan`. Possui dependências claras, agente dono e critérios de validação;
- **Capability:** Necessidade técnica que uma Task precisa satisfazer (ex: `data-cleaning`, `sql-analytics`, `data-quality`, `readme-generation`).

---

## 14. Agents

Os agentes nativos do AAF são especialistas funcionais coordenados pela fábrica. Suas atribuições são segregadas:

### 14.1 Agentes Core (Mandatórios no Ciclo Geral)
- **DiscoveryAgent:** Elicitação de requisitos, interface com usuário, gerenciamento de dúvidas (`Q-NN`) e premissas (`assumptions`);
- **ArchitectureAgent:** Síntese de requisitos, desenho técnico, definição de stack e governança de design;
- **PlannerAgent:** Decomposição estruturada em `ProjectPlan`, atribuição de `Tasks`, `Capabilities` e dependências;
- **DataAgent:** Ingestão de dados, sanitização, limpeza (`data-cleaning`), transformações e pipelines de dados;
- **DatabaseAgent:** DDL/DML, criação e migração de esquemas relacionais, modelagem dimensional e queries de persistência;
- **AnalyticsAgent:** Análise exploratória (EDA), agregações analíticas, SQL analítico, cálculo de métricas e visualizações;
- **TestingAgent:** Geração de testes automatizados (Pytest), validação sintática e asserções de qualidade de código;
- **DocumentationAgent:** Elaboração de documentação técnica, dicionários de dados, especificações e README oficial.

### 14.2 Agentes Condicionais (Ativados Exclusivamente sob Demanda Explícita)
- **BackendAgent:** Ativado apenas se o projeto analítico demandar uma API (ex: FastAPI) para exposição de endpoints analíticos;
- **FrontendAgent:** Ativado apenas se houver requisito expresso de interface gráfica web (ex: Streamlit/Dash);
- **ChatbotAgent:** Ativado apenas se a solução analítica incluir interface conversacional com o usuário final;
- **InfrastructureAgent:** Ativado apenas se a entrega requerer manifests de infraestrutura avançados (Terraform, Kubernetes, além do Dockerfile básico).

---

## 15. Skills / SkillIndex / SkillRouter / SkillRegistry

O subsistema de Skills fornece capacidades operacionais reutilizáveis e plugáveis:

1. **Skill:** Módulo funcional que encapsula uma capacidade atômica (ex: `data-cleaning`, `sql-analytics`, `data-quality`), implementando estritamente a interface `SkillContract` (`execute(context) -> SkillResult`);
2. **SkillIndex:** Catálogo declarativo compacto (`skill_index.yaml` e `SkillIndex`) contendo metadados de cada Skill: identificador canônico, capabilities atendidas, agentes autorizados (`allowed_agents`), dependências estruturais (`depends_on`) e triggers;
3. **SkillRouter:** Mecanismo determinístico de resolução. Recebe as capabilities de uma Task e:
   - Aplica a ordem de precedência: `preferred_skills` → `skill_id` explícito → match exato de capability → guardrails de domínio (`allowed_skills`) → guardrails de agente (`allowed_agents`) → sinônimos/triggers;
   - Realiza **seleção multi-skill (1..N)** para tarefas compostas;
   - Aplica **deduplicação inteligente** caso múltiplas capabilities convirjam para uma mesma skill;
   - Executa **ordenação topológica** respeitando as dependências estruturais (`depends_on`);
   - Bloqueia violações de segurança e escopo disparando `SkillRoutingError`;
4. **SkillRegistry:** Registro de execução. Realiza o **Lazy Loading** (carregamento progressivo de código e prompts) apenas no momento em que a Skill for efetivamente executada, evitando poluição de memória e de contexto dos agentes;
5. **Progressive Disclosure:** É expressamente proibido carregar o código-fonte de todas as Skills no contexto do LLM ou do agente. Apenas metadados trafegam pelo Router; o código só é instanciado na execução da Task.

---

## 16. MCPs (Model Context Protocol)

Os MCPs atuam como barramentos padronizados e controlados para que Agentes e Skills acessem recursos do ambiente:

- **Filesystem MCP:** Leitura e escrita restrita a diretórios autorizados pela política de paths (`PathPolicy`);
- **Database MCP:** Execução controlada de queries em bancos de dados aprovados, com sanitização de conexões;
- **Docker MCP:** Criação e gerenciamento de containers isolados para testes e runtime de dados.

**Limites Rígidos dos MCPs:**
- MCP é uma ferramenta de infraestrutura e acesso operacional;
- MCP **NÃO** decide arquitetura;
- MCP **NÃO** substitui Agentes nem Skills;
- MCP **NÃO** contém regras de negócio.

---

## 17. LLM Gateway

O **LLM Gateway** (`a_platform/j_llm_gateway/`) é o ponto centralizado e obrigatório para todas as chamadas a Modelos de Linguagem na plataforma:

1. **Abstração Total:** Isola completamente os Agentes e as Skills dos SDKs específicos (OpenAI, Anthropic, Google Gemini, Ollama, etc.);
2. **Acoplamento Proibido:** É categoricamente proibido importar bibliotecas de fornecedores de IA (`openai`, `anthropic`, `google.generativeai`) diretamente dentro de Agentes, Skills ou Contratos;
3. **Controle de Resiliência:** O Gateway gerencia timeouts, retries exponenciais, rotação de fallbacks configurados, contagem de tokens e auditoria de prompts.

---

## 18. Project Factory

A **Project Factory** (`a_platform/h_factory/`) coordena a esteira de construção dos componentes do projeto:

1. Recebe o `ProjectPlan` aprovado;
2. Itera sobre cada `Task` respeitando rigorosamente a ordem topológica e as dependências;
3. Instancia o Agente responsável e aciona as Skills roteadas via `SkillRegistry`;
4. Fornece contexto consolidado através do Brain e acessos via MCPs e LLM Gateway;
5. Recebe os `Artifacts` gerados em memória e os registra no `ExecutionContext`.

---

## 19. Artifacts

**Artifacts** são representações estruturadas e tipadas (`a_platform/b_contracts/g_artifact.py`) produzidas pelas Tasks e Skills:

1. Contêm metadados do arquivo: caminho relativo de destino, tipo de conteúdo (código Python, SQL, YAML, Markdown, Shell), permissões e hash de integridade;
2. São mantidos em memória durante a fase de geração na fábrica;
3. Representam a especificação formal antes da persistência física no sistema de arquivos;
4. Nenhum artefato é considerado válido se violar as diretrizes de código limpo, contratos de interface ou contiver placeholders.

---

## 20. Materializer

O **Materializer** (`a_platform/i_materializer/`) realiza a ponte entre os modelos lógicos e o sistema de arquivos:

1. **Destino Exclusivo:** Grava os `Artifacts` exclusivamente dentro do diretório do projeto:
   ```text
   e_generated_projects/<project_id>/
   ```
2. **Preservação de Estrutura:** Cria subdiretórios, grava scripts executáveis, datasets de exemplo, arquivos de configuração e documentação;
3. **Limites:** O Materializer é um componente mecânico de I/O. Ele **NÃO** interpreta requisitos, **NÃO** altera lógica de código e **NÃO** altera a arquitetura definida.

---

## 21. Runtime

O **Execution Runtime** (`a_platform/k_runtime/`) é responsável por colocar o projeto materializado à prova:

1. **Execução Real:** Executa os scripts gerados (Python, SQL, ETL) em ambiente real ou containerizado, jamais simulando respostas por mock;
2. **Captura Total de Evidências:** Registra para cada comando: código de saída (`exit_code`), tempo decorrido, `stdout`, `stderr` e artefatos de dados gerados;
3. **Isolamento e Segurança:** Aplica estritamente a política de comandos (`CommandPolicy`) e restrição de paths (`PathPolicy`), impedindo execução de instruções destrutivas ou acesso externo indevido.

---

## 22. Validation

O **Validation Gate** (`a_platform/l_validation/` e `ValidationGate`) audita a conformidade técnica do projeto gerado:

1. **Validação Estrutural:** Confere se todos os arquivos requeridos pelo `ProjectPlan` foram fisicamente materializados;
2. **Validação de Sintaxe e Compilação:** Executa checagem de integridade do código gerado;
3. **Validação de Execução:** Avalia se os pipelines rodaram com código `0` e geraram os outputs de dados esperados;
4. **Asserções de Negócio Analítico:** Verifica schemas das tabelas finais, volumetria gerada e ausência de dados corrompidos;
5. **Decisão:** Emite veredito formal (`status: PASSED` ou `status: FAILED` acompanhado de relatório de anomalias detalhado).

---

## 23. Quality

O **Quality Engine** (`a_platform/m_quality/`) avalia o projeto através de critérios de engenharia de software e engenharia de dados:

1. **Suíte de Testes:** Execução de testes unitários e de integração gerados pelo `TestingAgent` via Pytest;
2. **Qualidade de Dados:** Checagem de asserções de completude, unicidade e regras de dados;
3. **Integridade de Dependências:** Validação de compatibilidade e fixação de versões em `requirements.txt`;
4. **Higiene de Código:** Verificação de ausência de credenciais hardcoded, código morto ou construções inseguras;
5. **Veredito:** O gate de qualidade exige aprovação inequívoca baseada em evidências colhidas.

---

## 24. Certification

O **Certification Engine** (`a_platform/n_certification/`) é o gate final de prontidão da plataforma:

1. Realiza a auditoria cruzada de todas as etapas precedentes;
2. Inspeciona a cadeia de custódia das evidências coletadas desde o Discovery até o Quality;
3. Verifica se nenhum gate foi pulado, suprimido ou mascarado;
4. Somente emite `CertificationResult(status="PASSED")` se todos os critérios obrigatórios forem plenamente atendidos.

---

## 25. Repair and Recovery

O AAF adota uma política de resiliência e auto-recuperação determinística para falhas tratáveis.

### 25.1 Fluxo do Repair Contract
Diante de uma falha em qualquer gate ou execução de tarefa, o sistema deve seguir obrigatoriamente:

```text
FAILURE
    ↓
FAILURE DIAGNOSIS (análise de logs, stacktrace, stderr e validações)
    ↓
ROOT CAUSE IDENTIFICATION (diagnóstico da causa raiz técnica)
    ↓
RESPONSIBLE PHASE IDENTIFICATION (determinação da fase originária do defeito)
    ↓
INVALIDATE DOWNSTREAM (invalidação de todos os artefatos e gates posteriores)
    ↓
REPAIR (correção na fase responsável pelo agente correspondente)
    ↓
REPROCESS FROM RESPONSIBLE PHASE (re-execução ordenada a partir da fase corrigida)
    ↓
GATES NOVAMENTE (re-submissão integral a Runtime, Validation, Quality e Certification)
```

### 25.2 Tratamento de Causa Raiz Dependente do Usuário
Se a investigação da causa raiz determinar que a resolução depende de uma decisão humana indispensável (ex: ambiguidade irreconciliável de regra, credencial obrigatória, especificação de formato faltante):

```text
ROOT CAUSE
    ↓
REQUIRES USER INPUT
    ↓
NEEDS_INPUT
    ↓
PAUSED
    ↓
USER ANSWER
    ↓
RESUME
    ↓
RESPONSIBLE PHASE (reprocessamento a partir da fase de origem)
```

### 25.3 Limites e Proibição de Encerramento Precoce
- O loop de reparo possui tolerância máxima configurável de tentativas (padrão: 3 tentativas);
- **PROIBIÇÃO ABSOLUTA:** É terminantemente proibido adotar como fluxo normal o padrão:
  ```text
  FAIL ──► PROJECT READY = NO ──► FIM
  ```
- `PROJECT READY = NO` representa apenas o estado de **"ainda não pronto"** enquanto houver ciclo de reparo em andamento; não significa desistência automática sem esgotamento das etapas diagnósticas de reparo.
- O estado terminal `FAILED` só é admissível após o esgotamento formal das tentativas de reparo automático ou rejeição explícita do usuário.

---

## 26. NEEDS_INPUT / PAUSED / RESUME

O mecanismo de pausa interativa assegura que a fábrica nunca opere com premissas críticas falsas:

1. **Entrada em `NEEDS_INPUT`:** Ocorre quando um agente (notadamente `DiscoveryAgent`) detecta ausência de informação indispensável;
2. **Transição para `PAUSED`:** O orquestrador suspende a máquina de estados, persiste o checkpoint no `StateManager` (`h_runtime/state/`) e expõe a pergunta única na CLI ou interface da IDE;
3. **Recepção de `USER ANSWER`:** O usuário fornece a resposta pela interface oficial (`aaf resume` ou chat integrado);
4. **Ativação do `RESUME`:** O estado é reidratado do checkpoint, o dado é injetado no Brain e o fluxo é retomado exatamente a partir da fase que demandou o input, sem perda do progresso já certificado.

---

## 27. PROJECT READY

O status **`PROJECT READY = YES`** é o selo de prontidão de engenharia emitido pelo AAF.

### 27.1 Critérios Obrigatórios Cumulativos
O status `PROJECT READY = YES` só pode ser atribuído quando **todos** os seguintes marcos estiverem certificados por evidências reais:

- [x] **Discovery:** `COMPLETE` (requisitos estruturados, sem pendências bloqueantes);
- [x] **Planning:** `COMPLETE` (plano validado, tasks e dependências resolvidas);
- [x] **Materialization:** `SUCCESS` (arquivos físicos gravados e íntegros em disco);
- [x] **Execution:** `SUCCESS` / `PASS` (scripts rodaram com exit code 0 no Runtime);
- [x] **Validation:** `PASS` (todas as asserções e checagens contratuais aprovadas);
- [x] **Quality:** `PASS` (testes automatizados e requisitos de qualidade aprovados);
- [x] **Certification:** `PASS` (auditoria final do CertificationEngine aprovada).

### 27.2 Regra de Veracidade
`PROJECT READY` é uma **consequência factual de evidências coletadas**, nunca um valor arbitrário ou cosmético. Se qualquer gate obrigatório não tiver evidência de aprovação, o projeto permanece `PROJECT READY = NO`.

---

## 28. IDE Agent vs. Native Agents do AAF

Deve haver uma separação irrevogável e cristalina entre o agente de desenvolvimento da IDE e os agentes internos da plataforma AAF:

| Atributo | IDE Agent (Você / Antigravity / Cursor / Copilot) | AAF Native Agents (Discovery, Architecture, etc.) |
|---|---|---|
| **Papel** | Engenheiro de software auxiliando o desenvolvimento, manutenção e governança do código-fonte do AAF. | Agentes autônomos que operam a esteira do Golden Path para fabricar projetos analíticos. |
| **Escopo de Ação** | Edita arquivos da plataforma (`a_platform/`, `d_documentation/`, etc.) sob instrução explícita do desenvolvedor. | Executam tarefas planejadas, acionam Skills e geram Artifacts para `e_generated_projects/`. |
| **Interface com Usuário** | Ponto de transporte e facilitação de comandos (`aaf start`, `aaf resume`). | Processam prompts e lógica através do `LLM Gateway` e contratos da plataforma. |

### Proibições Específicas para o IDE Agent:
1. **NÃO emular internamente agentes do AAF:** O IDE Agent não deve "fingir" ser o `DiscoveryAgent` ou `ArchitectureAgent` gerando arquivos por fora da esteira;
2. **NÃO criar sucesso artificial:** O IDE Agent jamais deve forjar arquivos, mocks ou resultados para simular que a fábrica funcionou;
3. **NÃO editar manualmente o projeto gerado:** Se a geração do AAF falhar em `e_generated_projects/`, o IDE Agent **NÃO** deve corrigir o código gerado manualmente para disfarçar o erro do pipeline;
4. **NÃO bypassar o Repair Controller:** Correções devem ser realizadas pelo motor de reparo da própria plataforma, nunca por patches manuais da IDE durante o ciclo de fabricação;
5. **NÃO declarar `PROJECT READY`:** A declaração de prontidão cabe única e exclusivamente ao `CertificationEngine` do AAF via evidências reais.

---

## 29. Architecture Rules

As regras arquiteturais mestras da plataforma AAF são:

1. **Modular Monolith:** A estrutura interna da plataforma e os projetos analíticos gerados devem ser mantidos como Monolitos Modulares de alta coesão e baixo acoplamento;
2. **Princípio do Progressive Disclosure:** Informações detalhadas, código de skills e payloads pesados só devem ser carregados sob demanda explícita;
3. **Contratos Fortes e Tipados:** Todas as transições entre módulos dependem de modelos de dados tipados (`dataclasses` ou `pydantic`) definidos em `a_platform/b_contracts/`;
4. **Imutabilidade de Metadados de Execução:** Resultados de execuções de tasks e evidências de validação não devem ser mutados in-place; novas iterações criam novos registros versionados no `ExecutionContext`;
5. **Documentação Espelhada:** Qualquer alteração arquitetural deve ser devidamente refletida na documentação técnica (`d_documentation/b_documentation_technical/`) e funcional (`d_documentation/a_documentation_functional/`).

---

## 30. Guardrails

Guardrails são travas sistêmicas de segurança e estabilidade operacional:

1. **Domain Guardrails (`allowed_skills`):** Nenhum agente ou tarefa pode executar uma skill que não esteja explicitamente autorizada para o domínio configurado em `b_domains.yaml`;
2. **Agent Guardrails (`allowed_agents`):** Nenhuma skill pode ser invocada por um agente que não esteja listado em seus metadados (`allowed_agents` no `skill_index.yaml`);
3. **Path Guardrails (`PathPolicy`):** Todas as operações de leitura e escrita devem respeitar os limites do workspace e do projeto gerado, sendo terminantemente proibido acessar caminhos absolutos arbitrários do sistema operacional;
4. **Command Guardrails (`CommandPolicy`):** O Runtime só pode executar comandos aprovados em whitelist segura (Python, pytest, utilitários analíticos), bloqueando comandos de rede, instalação arbitrária não auditada ou operações privilegiadas (`sudo`, `rm -rf /`);
5. **Gate Integrity Guardrails:** É impossível avançar para a fase subsequente sem que a fase anterior tenha emitido status de conclusão válido.

---

## 31. Security Rules

1. **Segredos e Credenciais:** Nunca commitar, logar ou expor chaves de API, senhas ou tokens; usar sempre variáveis de ambiente (`.env` isolado);
2. **Sem Execução Shell Insegura:** Proibido uso de `shell=True` sem sanitização estrita ou interpolação de strings não higienizadas em comandos de terminal;
3. **Isolamento de Dados:** Dados do usuário depositados em `b_input/` devem ser manipulados em modo somente-leitura pelo profiling; transformações e limpezas operam sempre sobre cópias materializadas no projeto;
4. **Auditoria de Dependências:** O `TestingAgent` e a skill `dependency-quality` devem validar que bibliotecas externas declaradas nos projetos gerados possuem versões fixadas e livres de vulnerabilidades conhecidas.

---

## 32. Rules for Changing the AAF

Qualquer agente de desenvolvimento ou desenvolvedor que for modificar a plataforma AAF deve seguir esta disciplina:

1. **Inspeção Dupla (Produtor / Consumidor):** Antes de alterar qualquer contrato em `a_platform/b_contracts/` ou componente de plataforma, inspecionar obrigatoriamente tanto quem produz o dado quanto todos os consumidores existentes;
2. **Preservação de Legado Funcional:** Ao identificar estruturas divergentes ou complementares no repositório real, não deletar sem alinhamento e plano de migração explícito;
3. **Não Proliferação Desnecessária:** Não criar novos Agentes, Skills, MCPs ou provedores de LLM sem justificativa técnica indispensável aprovada arquiteturalmente;
4. **Documentação Sincronizada:** Qualquer alteração em contratos ou fluxos deve ser acompanhada da atualização dos arquivos markdown correspondentes em `d_documentation/`.

---

## 33. Definition of Ready (DoR)

Uma tarefa de fabricação ou implementação no AAF só pode ser iniciada quando:

1. Requisitos técnicos estiverem claramente delimitados e validados no Brain;
2. Contratos de entrada e saída estiverem estritamente definidos;
3. Domínio e guardrails estiverem estabelecidos;
4. Se envolver dados, o profiling inicial tiver sido concluído com evidências registradas;
5. Não houver impedimentos ou bloqueios ativos em `NEEDS_INPUT`.

---

## 34. Definition of Done (DoD)

Uma tarefa, funcionalidade ou ciclo de fabricação no AAF só é considerado concluído quando:

1. Todos os artefatos planejados foram gerados e materializados sem placeholders ou TODOs;
2. O código foi executado com sucesso no Runtime (exit code 0);
3. Todos os testes associados foram executados e aprovados;
4. Os gates de Validation, Quality e Certification emitiram veredito formal `PASSED`;
5. Nenhuma violação de arquitetura, contrato ou guardrail foi identificada;
6. O status formal `PROJECT READY = YES` foi atribuído com base em evidências verificadas.

---

## 35. Absolute Prohibitions (Proibições Absolutas)

As seguintes práticas são **estritamente proibidas** sob quaisquer circunstâncias:

1. **NÃO EXECUTAR COMANDOS GIT:** É expressamente proibido executar comandos Git em qualquer lugar deste projeto (`git status`, `git diff`, `git commit`, `git log`, etc.). Essa proibição é absoluta e irrevogável para agentes automatizados na IDE;
2. **NÃO GERAR FAKE SUCCESS:** Jamais reportar sucesso artificial, mockar retornos de gates ou disfarçar erros reais de execução;
3. **NÃO USAR PLACEHOLDERS OU MOCKS PERMANENTES:** Proibido código com `pass`, `# TODO: implementar depois` ou dados simulados em substituição à lógica de negócio analítica real;
4. **NÃO APLICAR FALLBACK SILENCIOSO:** Proibido capturar exceções silenciosamente (`except: pass`) transformando erros em status positivo sem tratamento e diagnóstico;
5. **NÃO INVENTAR REGRAS DE NEGÓCIO OU DADOS:** Proibido alucinar colunas, premissas de domínio ou esquemas não fundamentados em requisitos ou dados reais;
6. **NÃO ACOPLAR AGENTES DIRETAMENTE A SDKS DE LLM:** Nenhum agente ou skill pode importar provedores externos de IA fora do `LLM Gateway`;
7. **NÃO PULAR FASES DO GOLDEN PATH:** Proibido avançar sem passar pela sequência canônica de fases e seus respectivos gates de verificação;
8. **NÃO EXECUTAR FASES DEPENDENTES EM PARALELO:** Proibido disparar fases que dependam sequencialmente de outputs anteriores antes da consolidação formal da fase anterior;
9. **NÃO CRIAR MICROSERVIÇOS POR PADRÃO:** Proibido desmembrar o AAF ou os projetos gerados em microsserviços sem justificativa arquitetural explícita;
10. **NÃO IGNORAR A POLÍTICA DE PATHS E COMANDOS:** Proibido acessar diretórios arbitrários do sistema operacional ou executar comandos fora da whitelist de segurança;
11. **NÃO ENCERRAR AUTOMATICAMENTE COM FAIL SEM REPAIR:** Proibido adotar desistência imediata (`FAIL → PROJECT READY = NO → FIM`) diante de falhas recuperáveis sem antes acionar diagnóstico de causa raiz, invalidação downstream e reprocessamento;
12. **NÃO CONSTRUIR PROJETO MANUALMENTE PARA COBRIR FALHA DA AUTOMAÇÃO:** O IDE Agent jamais deve construir arquivos em `e_generated_projects/` para fingir que a plataforma funcionou quando o pipeline falhou. Se a automação falhou, a causa raiz na plataforma deve ser diagnosticada e corrigida.
