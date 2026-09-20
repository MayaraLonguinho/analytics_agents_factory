# Analytics Agents Factory — IDE Agent Contract

> **Documento Normativo Oficial — Constituição Operacional e Arquitetural do AAF**
>
> **Status:** Ativo / Mandatório para qualquer IDE Agent, AI Coding Agent ou Desenvolvedor.
>
> **Escopo de Aplicação:** Governança, desenvolvimento, refatoração, manutenção e operação do ecossistema Analytics Agents Factory (AAF).

---

## 1. Identidade

O **Analytics Agents Factory (AAF)** é uma plataforma multiagente determinística e modular projetada para a fabricação automatizada de projetos de software completos, executáveis e certificados no espaço de dados.

O AAF opera como um **Monolito Modular** de alta coesão e baixo acoplamento, regido por contratos estritos de dados, barramentos controlados de execução, guardrails arquiteturais e gates formais de validação.

No desenvolvimento e manutenção desta plataforma, qualquer agente de inteligência artificial ou desenvolvedor humano deve assumir a postura de **Principal Software Architect & AI Systems Architect**, zelando pela conformidade arquitetural, integridade conceitual e fidelidade estrita às regras aqui consagradas.

Este documento é normativo.

Em caso de conflito entre conveniência operacional de um IDE Agent e as regras deste contrato, prevalece este contrato.

---

## 2. Missão

A missão do AAF é transformar solicitações de usuários em linguagem natural — combinadas ou não com datasets brutos — em projetos analíticos estruturados, materializados em disco, efetivamente executados em ambiente de runtime, rigorosamente testados, validados contra contratos técnicos e formalmente certificados para entrega, sem intervenção manual de código e sem atalhos que comprometam a qualidade de engenharia.

---

## 3. Escopo Técnico

O AAF é especializado tecnicamente e de forma estrita nas seguintes disciplinas:

1. **Data Engineering:** ingestão de dados estruturados e semiestruturados, pipelines de ETL/ELT determinísticos, orquestração de fluxos de transformação, observabilidade e linhagem de pipelines;

2. **Analytics Engineering:** modelagem dimensional (Star Schema, Snowflake, tabelas fato e dimensões), modelagem em camadas modulares (raw, staging, intermediate, marts), views e agregações analíticas;

3. **Analytics & Data Analysis:** análise exploratória de dados (EDA), estatística descritiva, correlações, distribuição de variáveis, cálculo e agregação de KPIs e métricas de negócio, geração de visualizações e relatórios estruturados;

4. **Machine Learning Básica/Analítica, quando aplicável:** engenharia e seleção de features, treinamento supervisionado basilar, avaliação e inferência em lote;

5. **SQL Analítico & Otimização:** dialetos compatíveis com bancos relacionais e analíticos, incluindo PostgreSQL, DuckDB e SQLite, CTEs, window functions, planos de execução e indexação analítica;

6. **Qualidade & Validação de Dados:** asserções de integridade, completude, consistência, testes de schema, profiling e validação sintática/semântica;

7. **Documentação Técnica Automatizada:** especificações arquiteturais, dicionários de dados, linhagem e guias operacionais de execução.

---

## 4. Fora de Escopo

Estão expressamente **fora de escopo** do AAF:

1. **Regras de negócio arbitrárias ou inventadas:** o AAF é rigorosamente agnóstico ao domínio de negócio;

2. **Sistemas Web Full-Stack genéricos:** o AAF não é um gerador genérico de e-commerce, blogs, CRMs transacionais ou portais sociais;

3. **Microserviços distribuídos como padrão:** o padrão arquitetural é Modular Monolith;

4. **Alucinação de fontes e destinos críticos:** é vedado inventar conexões de produção, credenciais ou recursos externos inexistentes;

5. **Geração cosmética de código:** são proibidos pipelines vazios, placeholders permanentes, fake success ou implementações sem lógica analítica executável.

---

## 5. Contrato Funcional Oficial

O Contrato Funcional Oficial do AAF é:

> "O AAF recebe uma solicitação em linguagem natural, descobre e estrutura os requisitos, analisa os dados disponíveis quando aplicável, consolida o contexto no Brain, define a arquitetura, cria um ProjectPlan, decompõe o projeto em Tasks e Capabilities, atribui os Agents responsáveis, seleciona as Skills necessárias, estabelece a ordem e as dependências de execução, gera os Artifacts, materializa o projeto, executa o projeto realmente gerado e o conduz sequencialmente pelos gates de Validation, Quality e Certification. Quando uma falha recuperável ocorre, o AAF diagnostica a causa raiz, identifica a fase responsável, invalida os resultados posteriores afetados, retorna à fase responsável, corrige e reprocessa o fluxo. Quando uma decisão indispensável depende do usuário, o AAF entra em NEEDS_INPUT/PAUSED e continua após a resposta. O encerramento normal da fabricação ocorre somente quando todos os critérios de prontidão forem satisfeitos e PROJECT READY = YES, quando então o projeto funcional é entregue ao usuário."

Essa definição é inegociável.

---

## 6. Golden Path Oficial

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
BRAIN
    ↓
ARCHITECTURE
    ↓
PLANNER
    ↓
PROJECT PLAN
    ↓
PROJECT → TASKS [1..N]
    ↓
CAPABILITIES [1..N]
    ↓
AGENT ASSIGNMENT
    ↓
SKILL ROUTING
    ↓
SKILL INDEX
    ↓
DOMAIN / AGENT GUARDRAILS
    ↓
SKILLS [1..N]
    ↓
EXECUTION PLAN
    ↓
PROJECT FACTORY
    ↓
TASK 1 → AGENT → SKILLS → BRAIN/MCPs/LLM GATEWAY → ARTIFACTS
    ↓
TASK 2 → AGENT → SKILLS → BRAIN/MCPs/LLM GATEWAY → ARTIFACTS
    ↓
...
    ↓
TASK N → ARTIFACTS
    ↓
MATERIALIZER
    ↓
e_generated_projects/<project_id>/
    ↓
RUNTIME
    ↓
VALIDATION
    ↓
QUALITY
    ↓
CERTIFICATION
    ↓
PROJECT READY = YES
    ↓
RESULT
    ↓
PROJETO ENTREGUE AO USUÁRIO
```

### Restrição de Sequência Canônica

```text
Context → Plan → Decisions → Skills → Execution → Materialization → Gates
```

Fases dependentes não podem ser executadas antes da consolidação válida de suas dependências.

---

# 7. Repository Structure Governance

Esta seção governa a **estrutura física do próprio repositório Analytics Agents Factory**.

Estas regras aplicam-se principalmente ao IDE Agent, AI Coding Agent e desenvolvedores que modificam o código-fonte do AAF.

## 7.1 Root Directory Invariant

A raiz do repositório `analytics_agents_factory/` é uma **CLOSED ARCHITECTURAL BOUNDARY**.

A raiz:

- NÃO é workspace temporário;
- NÃO é área de scratch;
- NÃO é área de documentação;
- NÃO é área para diagramas;
- NÃO é área para arquivos Canvas;
- NÃO é área para relatórios;
- NÃO é área para backups;
- NÃO é área para outputs temporários de AI Agents;
- NÃO é área para artefatos gerados;
- NÃO é uma localização genérica para arquivos sem destino conhecido.

Nenhum Agent pode criar arbitrariamente novos arquivos ou diretórios diretamente na raiz.

Uma alteração na composição estrutural da raiz é considerada **ARCHITECTURAL CHANGE** e exige autorização humana explícita.

---

## 7.2 Canonical Root Structure

A estrutura raiz autorizada do AAF é:

```text
analytics_agents_factory/
├── .agents/
├── .obsidian/
├── a_platform/
├── b_input/
├── c_tests/
├── d_documentation/
├── e_generated_projects/
├── f_cli/
├── g_configuration/
├── h_runtime/
├── README.md
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

Os diretórios possuem responsabilidades arquiteturais distintas:

```text
.agents/
    contratos e instruções normativas para IDE/AI Agents

.obsidian/
    configuração técnica do workspace Obsidian

a_platform/
    implementação interna da plataforma AAF

b_input/
    fontes e datasets fornecidos como entrada

c_tests/
    testes da própria plataforma AAF

d_documentation/
    documentação funcional e técnica

e_generated_projects/
    projetos produzidos pelo Golden Path

f_cli/
    interface de linha de comando do AAF

g_configuration/
    configuração da plataforma e domínios

h_runtime/
    estado operacional de sessão do AAF
```

A presença desta árvore neste contrato **não autoriza sua recriação automática**.

---

## 7.3 Canonical Tree Is a Constraint, Not a Generation Template

A árvore estrutural documentada neste arquivo representa **limites arquiteturais autorizados**.

Ela NÃO deve ser interpretada como template de geração.

Antes de qualquer alteração, o Agent deve inspecionar a árvore física existente.

É proibido:

- criar automaticamente um diretório apenas porque aparece neste documento;
- recriar componente ausente sem investigar a implementação atual;
- duplicar estrutura equivalente já existente;
- criar uma segunda implementação de um componente porque o caminho esperado não foi encontrado;
- assumir que ausência de um path significa autorização para criá-lo.

Se um path esperado não existir, o Agent deve localizar o equivalente atual e inspecionar produtores e consumidores antes de qualquer decisão estrutural.

---

## 7.4 Existing Architecture Has Priority Over Convenience

Um IDE Agent deve adaptar sua implementação à arquitetura governada do AAF.

É proibido adaptar a arquitetura do AAF à conveniência da ferramenta.

Portanto:

```text
NECESSIDADE DE CRIAR ARQUIVO
        ↓
IDENTIFICAR OWNER ARQUITETURAL
        ↓
LOCALIZAR DESTINO CANÔNICO EXISTENTE
        ↓
VALIDAR NAMING
        ↓
VALIDAR BOUNDARY
        ↓
ESCREVER
```

Nunca:

```text
NECESSIDADE DE CRIAR ARQUIVO
        ↓
DESTINO INCERTO
        ↓
CRIAR NA RAIZ
```

---

## 7.5 File Ownership Rule

Todo arquivo criado deve possuir um **architectural owner**.

Exemplos:

| Tipo de artefato | Owner / destino |
|---|---|
| Regras de IDE Agent | `.agents/` |
| Configuração Obsidian | `.obsidian/` |
| Código da plataforma | `a_platform/` |
| Dataset de entrada | `b_input/` |
| Testes do AAF | `c_tests/` |
| Documentação funcional | `d_documentation/a_documentation_functional/` |
| Documentação técnica | `d_documentation/b_documentation_technical/` |
| Projeto fabricado | `e_generated_projects/<project_id>/` |
| CLI | `f_cli/` |
| Configuração | `g_configuration/` |
| Estado de sessão | `h_runtime/state/` |

Se não for possível determinar o owner arquitetural de um novo arquivo, o Agent **NÃO DEVE CRIÁ-LO**.

---

## 7.6 Root Write Policy

Antes de qualquer escrita diretamente em:

```text
analytics_agents_factory/
```

o Agent deve verificar se o nome alvo já pertence explicitamente à estrutura raiz canônica.

Caso contrário:

```text
ROOT WRITE = DENIED
```

Não é permitido criar na raiz, por exemplo:

```text
AAF Architeture Map.canvas
Architecture Map.canvas
Sem titulo.canvas
Untitled.canvas
analysis.md
notes.md
report.md
audit.md
temp.txt
draft.md
output.json
backup.py
copy.py
```

---

## 7.7 Naming Convention

Arquivos e diretórios controlados pelo AAF devem respeitar a convenção de naming da área arquitetural correspondente.

### Regras obrigatórias

1. Espaços em nomes de arquivos governados pelo AAF são proibidos;

2. Espaços em nomes de diretórios governados pelo AAF são proibidos;

3. Nomes genéricos são proibidos;

4. Nomes sem significado arquitetural são proibidos;

5. `snake_case` deve ser utilizado para nomes normais governados pelo AAF;

6. Nas áreas que utilizam ordenação por prefixos, novos arquivos e diretórios devem seguir o padrão de prefixação existente;

7. O Agent deve observar os irmãos do arquivo antes de escolher seu nome;

8. O Agent não pode introduzir uma segunda convenção de naming em uma pasta já governada por uma convenção existente.

### Nomes proibidos

Exemplos:

```text
Sem titulo.canvas
Sem Titulo.md
Untitled.md
New File.md
New Document.md
temp.py
temporary.py
draft.md
final.md
final_v2.md
copy.py
backup.py
teste novo.py
Architecture Map.canvas
AAF Architeture Map.canvas
```

### Exemplos estruturalmente válidos

Quando compatíveis com a convenção da pasta:

```text
a_architecture_map.canvas
b_golden_path.canvas
c_agent_architecture.md
d_runtime_flow.md
```

A validade do nome **não torna válido um destino incorreto**.

Um arquivo corretamente nomeado continua proibido se colocado em uma área arquitetural errada.

---

## 7.8 Prefix Governance

Prefixos são parte da organização arquitetural do AAF quando utilizados por uma área.

Exemplos:

```text
a_*
b_*
c_*
d_*
...
```

Antes de criar um arquivo ou diretório, o Agent deve inspecionar a convenção local.

Se a pasta utiliza prefixação ordenada, a nova entrada deve:

- utilizar prefixo coerente;
- não reutilizar prefixo conflitante;
- preservar ordenação semântica;
- não renumerar ou renomear estruturas existentes sem necessidade arquitetural;
- não criar prefixos arbitrários fora do padrão local.

---

## 7.9 Ecosystem-Required Exceptions

Arquivos cujo nome é imposto por linguagem, framework, ferramenta ou convenção externa podem ser exceções à regra de prefixação.

Exemplos:

```text
README.md
Dockerfile
docker-compose.yml
requirements.txt
pyproject.toml
.env.example
__init__.py
.gitkeep
```

Também podem existir arquivos internos de ferramentas como:

```text
.obsidian/*
```

quando seus nomes forem definidos pelo próprio ecossistema.

Uma exceção de naming **não é uma exceção de localização**.

---

## 7.10 Obsidian and Canvas Governance

O Obsidian é uma camada humana de documentação e visualização.

Arquivos `.canvas`:

- NÃO podem ser criados na raiz do repositório;
- NÃO podem receber nomes com espaços;
- NÃO podem receber nomes genéricos;
- NÃO podem ser criados automaticamente apenas porque a ferramenta suporta Canvas;
- NÃO podem duplicar uma visualização arquitetural existente;
- devem possuir destino documental autorizado;
- devem seguir a convenção de naming do local onde forem armazenados.

Antes de criar um Canvas, o Agent deve verificar:

1. se o Canvas é realmente necessário;
2. se já existe visualização equivalente;
3. qual área documental é dona da visualização;
4. qual naming convention essa área utiliza;
5. se o conteúdo está sustentado pela arquitetura e implementação reais.

Um Canvas nunca se torna SSOT apenas por ter sido gerado.

---

## 7.11 No Orphan Artifacts

Todo novo arquivo deve possuir pelo menos uma finalidade verificável dentro da arquitetura.

São proibidos **orphan artifacts**, incluindo:

- Canvas vazios;
- Markdown sem owner;
- relatórios temporários;
- arquivos de análise abandonados;
- arquivos de auditoria não solicitados;
- cópias de segurança produzidas pelo Agent;
- versões `v2`, `final`, `new`, `copy`;
- outputs intermediários sem consumidor;
- documentação duplicada.

Um arquivo vazio ou sem consumidor arquitetural deve ser considerado suspeito e não deve ser criado automaticamente.

---

## 7.12 Pre-Write Structural Validation

Antes de executar QUALQUER operação que crie um novo arquivo ou diretório no repositório AAF, o IDE Agent deve executar conceitualmente o seguinte gate:

```text
PRE-WRITE STRUCTURAL VALIDATION

1. NECESSARY?
   O artefato é realmente necessário?
        ↓
2. OWNER?
   Qual domínio arquitetural é responsável?
        ↓
3. DESTINATION?
   Existe destino canônico?
        ↓
4. BOUNDARY?
   O destino está autorizado?
        ↓
5. NAMING?
   O nome segue a convenção local?
        ↓
6. PREFIX?
   O prefixo está correto quando aplicável?
        ↓
7. DUPLICATE?
   Já existe artefato equivalente?
        ↓
8. CONSUMER?
   Existe uso ou finalidade arquitetural?
        ↓
WRITE ALLOWED
```

Se qualquer uma dessas validações falhar:

```text
DO NOT WRITE
```

O Agent deve corrigir o plano antes de criar o arquivo.

---

## 7.13 Pre-Move and Pre-Rename Validation

As mesmas regras aplicam-se a:

- mover;
- copiar;
- renomear;
- duplicar;
- restaurar;
- converter;
- gerar versão alternativa de arquivo.

Um `move` não pode ser utilizado para introduzir um arquivo em localização proibida.

Um `rename` não pode quebrar referências, imports, documentação ou consumidores.

---

## 7.14 No Opportunistic Structure Changes

Durante uma tarefa, é proibido realizar alterações estruturais oportunistas não solicitadas.

O Agent NÃO deve:

- criar convenience folders;
- reorganizar diretórios por preferência pessoal;
- criar pastas auxiliares;
- criar arquivos scratch;
- criar backups;
- criar cópias;
- criar documentação adicional não necessária;
- criar relatórios de auditoria não solicitados;
- criar novos Canvas por conveniência;
- criar nova camada arquitetural;
- mover componentes funcionais sem necessidade;
- "melhorar" a árvore fora do escopo solicitado.

---

## 7.15 Structural Change Requires Explicit Authorization

São consideradas alterações arquiteturais estruturais:

- novo diretório na raiz;
- novo arquivo permanente na raiz;
- remoção de diretório raiz;
- mudança de responsabilidade entre diretórios;
- introdução de nova camada arquitetural;
- mudança global de naming convention;
- mudança global de prefixos;
- criação de novo subsistema paralelo.

Essas mudanças exigem autorização humana explícita.

---

## 8. Estados Operacionais

O `StateManager` reconhece:

| Estado | Descrição |
|---|---|
| `INITIALIZED` | Projeto criado e contexto instanciado. |
| `DISCOVERY` | Levantamento de requisitos. |
| `NEEDS_INPUT` | Informação indispensável requerida. |
| `PAUSED` | Sessão suspensa aguardando interação. |
| `RESUMED` | Sessão retomada. |
| `PROFILING` | Análise técnica do dataset. |
| `ARCHITECTING` | Arquitetura técnica. |
| `PLANNING` | ProjectPlan, Tasks, Capabilities e Skills. |
| `GENERATING` | ProjectFactory produzindo Artifacts. |
| `MATERIALIZING` | Persistência física do projeto. |
| `EXECUTING` | Runtime executando o projeto. |
| `VALIDATING` | Validation Gate. |
| `REPAIRING` | Diagnóstico, correção e reprocessamento. |
| `QUALITY_CHECK` | Quality Engine. |
| `CERTIFYING` | Certification Engine. |
| `READY` | `PROJECT READY = YES`. |
| `FAILED` | Estado terminal anômalo após impossibilidade formal de recuperação. |

---

## 9. Discovery Protocol

O `DiscoveryAgent` deve:

1. Fazer no máximo 5 perguntas;
2. Fazer exatamente uma pergunta por vez;
3. Perguntar apenas quando a resposta alterar arquitetura, escopo, capability, source, target, aceitação ou decisão técnica indispensável;
4. Converter incertezas menores em assumptions explícitas;
5. Registrar dúvidas pendentes como `Q-01`, `Q-02`, etc.;
6. Nunca inventar regras de negócio;
7. Entrar em `NEEDS_INPUT → PAUSED` quando faltar informação indispensável;
8. Retomar na fase responsável após resposta.

---

## 10. Dataset Profiling

Quando houver dataset disponível, o `DatasetProfilingSkill` deve operar antes da definição arquitetural dependente desses dados.

Deve coletar evidências reais, incluindo:

- linhas e colunas;
- nomes literais das colunas;
- tipos;
- cardinalidade;
- nulos;
- duplicados;
- anomalias de formatação;
- evidências necessárias ao planejamento.

É proibido presumir schema fictício quando dados reais estiverem disponíveis.

Quando não houver dataset aplicável, a fase deve ser tratada explicitamente como não aplicável, sem inventar evidência.

---

## 11. Brain

O Brain é a **Single Source of Truth operacional** do projeto durante a fabricação.

Pode consolidar:

- `context`;
- `requirements`;
- `evidence`;
- `rules`;
- `patterns`;
- `domains`;
- `decisions`;
- `graph`.

### Brain vs. Obsidian

`a_platform/c_brain/` representa contexto operacional consumido pela plataforma.

`.obsidian/` e documentação associada representam visualização e navegação humanas.

Obsidian:

- NÃO executa lógica;
- NÃO decide arquitetura;
- NÃO substitui o Brain;
- NÃO é dependência obrigatória do Golden Path.

---

## 12. Architecture

O `ArchitectureAgent` é responsável por:

- stack;
- estrutura do projeto gerado;
- convenções;
- SQL dialect;
- padrões analíticos;
- guardrails arquiteturais.

A arquitetura padrão é Modular Monolith.

Frameworks, serviços ou componentes não catalogados não devem ser introduzidos arbitrariamente.

---

## 13. Planning

O `PlannerAgent` traduz arquitetura em `ProjectPlan`.

Para cada Task, define:

- entrega;
- Agent;
- Capabilities `[1..N]`;
- Skills `[1..N]`;
- MCPs quando necessários;
- `depends_on`;
- critérios de aceitação;
- evidências esperadas.

O Planner é responsável pela decomposição e dependências.

O SkillRouter é responsável pela resolução de Skills, não pela orquestração global do projeto.

---

## 14. Project / Task / Capability

```text
1 Project → 1..N Tasks

1 Task → 1..N Capabilities

1 Task → 1 Agent responsável

1 Task → 1..N Skills quando necessárias
```

Capability representa a necessidade.

Skill representa uma implementação reutilizável dessa necessidade.

---

## 15. Agents

### Core

- `DiscoveryAgent`
- `ArchitectureAgent`
- `PlannerAgent`
- `DataAgent`
- `DatabaseAgent`
- `AnalyticsAgent`
- `TestingAgent`
- `DocumentationAgent`

### Condicionais

- `BackendAgent`
- `FrontendAgent`
- `ChatbotAgent`
- `InfrastructureAgent`

Agentes condicionais somente devem ser utilizados quando requeridos pelo projeto.

---

## 16. Skills / SkillIndex / SkillRouter / SkillRegistry

### Skill

Capability operacional reutilizável.

### SkillIndex

Catálogo compacto de metadados.

### SkillRouter

Resolve uma ou mais Skills necessárias para as Capabilities da Task, respeitando:

- preferências explícitas válidas;
- capability;
- domínio;
- `allowed_skills`;
- Agent;
- `allowed_agents`;
- dependências;
- deduplicação;
- triggers quando necessários.

### SkillRegistry

Autoridade de resolução da implementação executável.

### Progressive Disclosure

Metadados compactos podem ser consultados para routing.

Implementação, prompts e recursos pesados devem ser carregados somente quando necessários.

É proibido carregar indiscriminadamente todas as Skills no contexto.

---

## 17. MCPs

MCPs fornecem acesso operacional controlado.

MCPs homologados incluem:

- Filesystem;
- Database;
- Docker.

MCP:

- NÃO decide arquitetura;
- NÃO substitui Agent;
- NÃO substitui Skill;
- NÃO contém regra de negócio.

---

## 18. LLM Gateway

O LLM Gateway centraliza integrações com modelos.

Agents e Skills não devem depender diretamente de SDKs de providers.

Providers somente podem ser utilizados quando implementados e habilitados na configuração real.

É proibido inventar fallback ou provider inexistente.

---

## 19. Project Factory

A Project Factory:

1. recebe `ProjectPlan`;
2. respeita dependências;
3. executa Tasks na ordem válida;
4. instancia Agents;
5. resolve Skills pelo Registry;
6. disponibiliza Brain/MCP/LLM Gateway quando necessários;
7. recebe Artifacts.

Execução paralela somente pode existir quando explicitamente segura e permitida pelas dependências do plano.

Nunca se deve paralelizar fases dependentes do Golden Path.

---

## 20. Artifacts

Artifacts são representações tipadas anteriores à materialização.

Devem conter:

- path relativo;
- tipo;
- conteúdo;
- metadados necessários;
- integridade.

Artifacts inválidos, placeholders ou caminhos proibidos devem ser rejeitados.

---

## 21. Materializer

O Materializer escreve exclusivamente o projeto fabricado dentro de:

```text
e_generated_projects/<project_id>/
```

O Materializer não deve escrever arquivos de manutenção do próprio repositório AAF.

O Materializer:

- NÃO interpreta requisitos;
- NÃO altera arquitetura;
- NÃO inventa novos destinos;
- NÃO grava projetos gerados na raiz;
- NÃO grava fora do `project_id`.

---

## 22. Runtime

O Runtime executa o projeto materializado de forma real.

Deve capturar evidências como:

- `exit_code`;
- `stdout`;
- `stderr`;
- duração;
- outputs gerados.

Execução deve respeitar `CommandPolicy` e `PathPolicy`.

Execução insegura com `shell=True` não deve ser utilizada.

---

## 23. Validation

Validation deve verificar:

- estrutura;
- sintaxe;
- execução;
- outputs;
- schemas;
- critérios de aceitação.

Falha gera evidência e aciona Repair quando recuperável.

---

## 24. Quality

Quality avalia evidências de:

- testes;
- qualidade de dados;
- dependências;
- higiene de código;
- segurança aplicável;
- critérios definidos pelo ProjectPlan.

Nenhum resultado pode ser aprovado sem evidência real.

---

## 25. Certification

Certification é o gate final.

Somente pode aprovar quando todos os critérios obrigatórios anteriores possuírem evidências válidas.

Nenhum gate pode ser mascarado ou artificialmente marcado como aprovado.

---

## 26. Repair and Recovery

```text
FAILURE
    ↓
FAILURE DIAGNOSIS
    ↓
ROOT CAUSE IDENTIFICATION
    ↓
RESPONSIBLE PHASE IDENTIFICATION
    ↓
INVALIDATE DOWNSTREAM
    ↓
REPAIR
    ↓
REPROCESS FROM RESPONSIBLE PHASE
    ↓
RUNTIME / VALIDATION / QUALITY / CERTIFICATION
```

Quando a resolução depender de informação humana:

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
RESPONSIBLE PHASE
```

`PROJECT READY = NO` significa "ainda não pronto" enquanto houver recuperação válida possível.

Não é o caminho normal de encerramento.

---

## 27. NEEDS_INPUT / PAUSED / RESUME

Quando faltar informação indispensável:

```text
NEEDS_INPUT → PAUSED → USER ANSWER → RESUME → RESPONSIBLE PHASE
```

Checkpoint operacional pertence a:

```text
h_runtime/state/
```

Esse diretório contém somente estado operacional previsto.

Não deve ser utilizado para documentação, relatórios ou arquivos temporários arbitrários.

---

## 28. PROJECT READY

`PROJECT READY = YES` exige cumulativamente:

- Discovery COMPLETE;
- Planning COMPLETE;
- Materialization SUCCESS;
- Execution SUCCESS;
- Validation PASS;
- Quality PASS;
- Certification PASS.

Readiness é consequência de evidência, nunca flag cosmética.

---

## 29. IDE Agent vs. Native Agents

O IDE Agent desenvolve e mantém o AAF.

Os Native Agents executam o AAF.

O IDE Agent:

- NÃO deve fingir ser Native Agent;
- NÃO deve gerar projeto manualmente para mascarar falha;
- NÃO deve corrigir manualmente um projeto gerado para esconder defeito da fábrica;
- NÃO deve declarar `PROJECT READY`;
- NÃO deve bypassar Repair;
- NÃO deve criar artefatos do Golden Path fora da arquitetura oficial.

---

## 30. Architecture Rules

1. Modular Monolith;

2. Progressive Disclosure;

3. Contratos fortes e tipados;

4. Evidências reais;

5. Separação entre planejamento, execução e certificação;

6. Brain como SSOT operacional;

7. Obsidian como visualização humana;

8. Estrutura física governada;

9. Naming governado;

10. Nenhuma mudança arquitetural oportunista;

11. Documentação sincronizada quando uma mudança arquitetural real for autorizada.

---

## 31. Guardrails

### Domain Guardrails

Skills devem respeitar `allowed_skills`.

### Agent Guardrails

Skills devem respeitar `allowed_agents`.

### Path Guardrails

Operações devem respeitar `PathPolicy`.

### Command Guardrails

Execuções devem respeitar `CommandPolicy`.

### Gate Integrity

Uma fase dependente não avança sem output válido da anterior.

### Repository Structure Guardrail

Qualquer escrita no repositório deve respeitar:

```text
canonical_tree
+ architectural_owner
+ destination_policy
+ naming_policy
+ prefix_policy
+ no_duplicate_policy
```

### Root Guardrail

Qualquer tentativa não autorizada de introduzir novo arquivo ou diretório na raiz deve ser bloqueada.

### Naming Guardrail

Qualquer nome com:

- espaços proibidos;
- nome genérico;
- convenção incompatível;
- ausência de prefixo obrigatório;

deve ser rejeitado antes da escrita.

---

## 32. Security Rules

1. Nunca expor secrets;

2. Não utilizar `shell=True` inseguro;

3. Não acessar paths arbitrários;

4. Dados de entrada devem ser preservados;

5. Operações destrutivas devem ser bloqueadas;

6. Nenhuma ferramenta pode bypassar `PathPolicy`;

7. Nenhum mecanismo de geração pode escrever fora de seu boundary autorizado.

---

## 33. Rules for Changing the AAF

Antes de modificar o AAF:

### 33.1 Inspect Before Change

Sempre inspecionar a implementação real antes de editar.

Nunca assumir estrutura somente por documentação histórica.

### 33.2 Producer / Consumer Inspection

Antes de modificar contrato ou interface, verificar produtores e consumidores.

### 33.3 Locate Before Create

Se um componente esperado não estiver no path imaginado:

```text
SEARCH CURRENT IMPLEMENTATION
```

antes de:

```text
CREATE NEW IMPLEMENTATION
```

### 33.4 Preserve Functional Behavior

Não destruir comportamento funcional comprovado por conveniência de refatoração.

### 33.5 No Parallel Architecture

Não criar:

- segundo Registry;
- segundo Router;
- segundo Brain;
- segundo Runtime;
- segundo sistema de Contracts;
- segundo pipeline equivalente;

sem decisão arquitetural explícita.

### 33.6 Minimal Change Principle

Alterar somente o necessário para resolver a causa raiz ou implementar o requisito solicitado.

### 33.7 Structural Compliance

Antes de criar arquivo:

```text
inspect tree
→ identify owner
→ identify destination
→ validate naming
→ validate prefix
→ validate duplicate
→ write
```

### 33.8 Documentation Synchronization

Mudanças arquiteturais autorizadas devem ser refletidas na documentação correspondente.

Não criar documentação extra na raiz como mecanismo de registro da mudança.

---

## 34. Definition of Ready — DoR

Uma tarefa só pode iniciar quando:

1. requisito está delimitado;
2. contratos relevantes estão identificados;
3. guardrails são conhecidos;
4. evidências necessárias estão disponíveis;
5. não há `NEEDS_INPUT` bloqueante;
6. para alterações no AAF, o owner e o destino estrutural estão identificados.

---

## 35. Definition of Done — DoD

Para fabricação de projeto pelo Golden Path:

1. Artifacts válidos;
2. Materialization concluída;
3. Runtime executado;
4. Validation PASS;
5. Quality PASS;
6. Certification PASS;
7. `PROJECT READY = YES`.

Para uma alteração de desenvolvimento no próprio AAF, adicionalmente:

1. nenhum arquivo órfão foi criado;
2. nenhuma alteração estrutural não autorizada foi introduzida;
3. naming permanece conforme convenção;
4. raiz permanece conforme arquitetura canônica;
5. documentação relevante permanece coerente.

---

# 36. Absolute Prohibitions

As seguintes práticas são estritamente proibidas:

1. **NÃO EXECUTAR COMANDOS GIT** por Agents automatizados da IDE;

2. **NÃO GERAR FAKE SUCCESS**;

3. **NÃO UTILIZAR PLACEHOLDERS OU MOCKS PERMANENTES**;

4. **NÃO APLICAR FALLBACK SILENCIOSO**;

5. **NÃO INVENTAR REGRAS DE NEGÓCIO OU DADOS**;

6. **NÃO ACOPLAR AGENTS/SKILLS DIRETAMENTE A SDKs DE LLM**;

7. **NÃO PULAR FASES DEPENDENTES DO GOLDEN PATH**;

8. **NÃO EXECUTAR FASES DEPENDENTES EM PARALELO**;

9. **NÃO CRIAR MICROSERVIÇOS POR PADRÃO**;

10. **NÃO IGNORAR PATHPOLICY OU COMMANDPOLICY**;

11. **NÃO ENCERRAR FALHA RECUPERÁVEL SEM REPAIR**;

12. **NÃO CONSTRUIR PROJETO MANUALMENTE PARA COBRIR FALHA DA AUTOMAÇÃO**;

13. **NÃO CRIAR NOVOS ARQUIVOS OU DIRETÓRIOS ARBITRARIAMENTE NA RAIZ**;

14. **NÃO UTILIZAR A RAIZ COMO SCRATCH, OUTPUT, DOCUMENTATION OU CANVAS DIRECTORY**;

15. **NÃO CRIAR ARQUIVOS COM ESPAÇOS EM NOMES GOVERNADOS PELO AAF**;

16. **NÃO CRIAR ARQUIVOS COM NOMES GENÉRICOS**, incluindo `Untitled`, `Sem titulo`, `temp`, `draft`, `copy`, `backup`, `new`, `final` e equivalentes;

17. **NÃO IGNORAR PREFIXOS OBRIGATÓRIOS** quando a pasta de destino utilizar convenção ordenada;

18. **NÃO CRIAR ARQUIVOS SEM ARCHITECTURAL OWNER**;

19. **NÃO CRIAR ORPHAN ARTIFACTS**;

20. **NÃO CRIAR CANVAS NA RAIZ**;

21. **NÃO CRIAR CANVAS VAZIO OU DUPLICADO**;

22. **NÃO CRIAR NOVA PASTA POR CONVENIÊNCIA DO AGENT**;

23. **NÃO INTERPRETAR A CANONICAL TREE COMO TEMPLATE DE GERAÇÃO**;

24. **NÃO RECRIAR COMPONENTE AUSENTE ANTES DE PROCURAR SEU EQUIVALENTE ATUAL**;

25. **NÃO INTRODUZIR SEGUNDA IMPLEMENTAÇÃO PARALELA DE COMPONENTE EXISTENTE**;

26. **NÃO MOVER OU RENOMEAR COMPONENTES ARQUITETURAIS FORA DO ESCOPO SOLICITADO**;

27. **NÃO CRIAR RELATÓRIOS, AUDITORIAS OU DOCUMENTAÇÃO AUXILIAR NÃO SOLICITADOS**;

28. **NÃO ALTERAR A COMPOSIÇÃO DA RAIZ SEM AUTORIZAÇÃO HUMANA EXPLÍCITA**.

---

# 37. Mandatory Pre-Write Gate for IDE Agents

Esta regra deve ser aplicada pelo IDE Agent antes de toda criação de arquivo.

```text
┌─────────────────────────────────────┐
│ NEW FILE / DIRECTORY REQUEST        │
└──────────────────┬──────────────────┘
                   ↓
        ┌─────────────────────┐
        │ Is it necessary?    │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Who owns it?        │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Canonical location? │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Boundary allowed?   │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Naming valid?       │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Prefix valid?       │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Duplicate exists?   │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ Consumer/purpose?   │
        └──────────┬──────────┘
                   ↓
              WRITE ALLOWED
```

Se qualquer resposta necessária for negativa ou indeterminada:

```text
DO NOT WRITE
```

O Agent deve primeiro resolver a inconsistência estrutural.

---

# 38. Structural Invariant

Ao final de qualquer intervenção do IDE Agent, deve continuar verdadeira a seguinte propriedade:

```text
CURRENT REPOSITORY
        ⊆
AUTHORIZED AAF ARCHITECTURE
```

e:

```text
NEW ARTIFACT
    =
NECESSARY
+ OWNED
+ CANONICALLY LOCATED
+ CORRECTLY NAMED
+ NON-DUPLICATED
+ ARCHITECTURALLY JUSTIFIED
```

Nunca:

```text
NEW ARTIFACT
    =
TOOL CONVENIENCE
```

---

# 39. Final Governing Principle

O AAF deve permanecer estruturalmente previsível.

Um Agent não possui autoridade para inventar arquitetura física.

Toda alteração deve respeitar:

```text
INTENT
    ↓
EXISTING ARCHITECTURE
    ↓
CONTRACTS
    ↓
GUARDRAILS
    ↓
MINIMAL VALID CHANGE
    ↓
EVIDENCE
```

A arquitetura existente deve ser **inspecionada antes de ser modificada, preservada antes de ser expandida e governada antes de ser automatizada**.