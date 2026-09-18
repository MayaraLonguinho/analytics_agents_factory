# Analytics Agents Factory (AAF)

## 1. Visão Geral

O **Analytics Agents Factory (AAF)** é uma plataforma multiagente especializada na geração automatizada de projetos de **Analytics e Data Engineering**.

O AAF recebe uma solicitação em linguagem natural, analisa requisitos e dados, define uma arquitetura, planeja a execução, coordena Agents especializados e materializa um projeto estruturado.

A proposta da plataforma não é apenas gerar código. O fluxo foi projetado para também executar, validar, avaliar qualidade e certificar o projeto produzido.

Em resumo:

**Intenção → Planejamento → Geração → Execução → Validação → Projeto**

---

## 2. Objetivo

O objetivo do AAF é transformar uma necessidade de Analytics ou Data Engineering em um projeto executável utilizando uma fábrica composta por:

- **Brain** — contexto, regras, padrões, domínios e decisões;
- **Agents** — especialistas responsáveis por diferentes etapas;
- **Skills** — capacidades reutilizáveis utilizadas pelos Agents;
- **MCPs** — interfaces controladas para recursos operacionais;
- **LLM Gateway** — abstração para utilização de modelos de linguagem;
- **Project Factory** — coordenação da geração;
- **Materializer** — criação física dos arquivos;
- **Runtime** — execução do projeto gerado;
- **Validation** — validação estrutural e de execução;
- **Quality** — avaliação das evidências de qualidade;
- **Certification** — gate final de prontidão.

O AAF é **agnóstico ao domínio de negócio**, mas especializado tecnicamente em **Analytics e Data Engineering**.

---

## 3. Como Funciona

O Golden Path conceitual do AAF é:

```text
IDE Chat / CLI
      ↓
Discovery
      ↓
Dataset Profiling
      ↓
Brain
      ↓
Architecture
      ↓
Planner
      ↓
Project Factory
      ↓
Agents
 ┌────┼─────┐
Skills MCPs LLM
 └────┼─────┘
      ↓
Artifacts
      ↓
Materializer
      ↓
e_generated_projects/
      ↓
Runtime
      ↓
Validation
      │
      └── FAIL → Repair Loop
      ↓
Quality
      ↓
Certification
      ↓
PROJECT READY
```

### Discovery

O `DiscoveryAgent` entende a solicitação, coleta requisitos relevantes e pode pausar a sessão quando uma decisão do usuário é necessária.

Dataset Profiling

Quando existe um dataset, o DatasetProfilingSkill utiliza Pandas para obter evidências reais como:

quantidade de registros;
quantidade de colunas;
nomes das colunas;
tipos;
duplicidades;
warnings relevantes.
Brain

O Brain funciona como o SSOT operacional de conhecimento e contexto do AAF.

Ele organiza:

contexto;
regras;
padrões;
domínios;
decisões;
relações entre conhecimentos.
Architecture

O ArchitectureAgent utiliza os requisitos, o profiling e o contexto do Brain para definir a arquitetura técnica do projeto.

Planner

O PlannerAgent transforma a arquitetura em um ProjectPlan, definindo:

tarefas;
Agents;
Skills;
MCPs;
artifacts;
comandos;
evidências necessárias.
Project Factory

A ProjectFactory distribui as tarefas planejadas entre os Agents especializados e reúne os Artifacts produzidos.

Materializer

O Materializer transforma os Artifacts lógicos em arquivos físicos dentro de:

e_generated_projects/<project_id>/
Runtime

O Runtime executa os comandos necessários do projeto gerado de forma controlada.

Validation e Repair Loop

O Validation verifica estrutura e evidências de execução.

Quando ocorre uma falha recuperável, o Repair Loop pode solicitar uma correção, materializar novamente, executar novamente e revalidar.

Quality

O Quality Engine avalia evidências relacionadas a testes, qualidade de código, segurança e dependências.

Certification

O Certification Engine consolida os gates obrigatórios.

A regra conceitual é:

Discovery        COMPLETE
Planning         COMPLETE
Materialization  SUCCESS
Execution        SUCCESS
Validation       PASS
Quality          PASS
Certification    PASS
        ↓
PROJECT READY = YES

Caso algum gate obrigatório falhe:

PROJECT READY = NO
4. Estrutura do Projeto
analytics_agents_factory/
├── .agents/
├── .obsidian/
├── a_platform/
│   ├── b_contracts/
│   ├── c_brain/
│   ├── e_skills/
│   ├── f_mcps/
│   ├── g_agents/
│   ├── h_factory/
│   ├── i_materializer/
│   ├── j_llm_gateway/
│   ├── k_runtime/
│   ├── l_validation/
│   ├── m_quality/
│   ├── n_certification/
│   └── o_orchestration/
├── b_input/
├── c_tests/
├── d_documentation/
│   ├── a_documentation_functional/
│   └── b_documentation_technical/
├── e_generated_projects/
├── f_cli/
├── g_configuration/
├── h_runtime/
│   └── state/
├── README.md
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
5. Principais Pastas
.agents/

Contém regras e instruções utilizadas no desenvolvimento e manutenção do AAF.

.obsidian/

Contém a configuração do workspace utilizado para visualização da documentação e do grafo de conhecimento através do Obsidian.

a_platform/

É o núcleo funcional da plataforma.

b_contracts/

Define os contratos compartilhados entre os componentes.

Entre eles:

Project
AgentContract
SkillContract
MCPContract
Task
ProjectPlan
Artifact
Execution
ExecutionContext
State
Validation
Quality
Certification
c_brain/

Implementa o Brain do AAF.

c_brain/
├── a_context/
├── b_rules/
├── c_patterns/
├── d_domains/
├── e_decisions/
├── f_graph/
├── g_brain.py
└── h_learning_engine.py

O LearningEngine existe estruturalmente, mas está fora do Golden Path operacional atual.

e_skills/

Contém as capacidades reutilizáveis dos Agents.

e_skills/
├── a_dataset_profiling/
├── b_etl/
├── c_sql/
├── d_analytics/
├── e_quality/
├── f_documentation/
├── g_optional/
└── h_registry/

Conceitualmente:

Agent
  ↓
SkillRegistry
  ↓
Skill
  ↓
validate_input
  ↓
execute
  ↓
validate_output

Agent é quem executa uma responsabilidade.
Skill é aquilo que o Agent sabe fazer.

f_mcps/

Contém os MCPs disponíveis:

f_mcps/
├── a_filesystem/
├── b_database/
├── c_docker/
└── d_registry/

Os MCPs representam interfaces controladas para interação com recursos operacionais.

g_agents/

Contém os especialistas da fábrica.

g_agents/
├── a_base/
├── b_discovery/
├── c_architecture/
├── d_planner/
├── e_data/
├── f_database/
├── g_analytics/
├── h_testing/
├── i_documentation/
├── j_backend/
├── k_frontend/
├── l_chatbot/
├── m_infrastructure/
├── n_factory/
├── o_registry/
└── p_declarations/

Agents principais:

DiscoveryAgent
ArchitectureAgent
PlannerAgent
DataAgent
DatabaseAgent
AnalyticsAgent
TestingAgent
DocumentationAgent

Agents como Backend, Frontend, Chatbot e Infrastructure são condicionais e dependem das necessidades do projeto.

h_factory/

Contém a ProjectFactory, responsável por coordenar a geração dos Artifacts através dos Agents.

i_materializer/

Responsável por transformar Artifacts em arquivos físicos.

Também aplica políticas para controlar os caminhos onde os arquivos podem ser materializados.

j_llm_gateway/

Abstrai a utilização dos modelos de linguagem.

Agent / Skill
     ↓
LLM Gateway
     ↓
Provider

O objetivo é impedir que Agents e Skills fiquem diretamente acoplados a um fornecedor específico.

No Golden Path atual, o provider operacional é OpenAI.

Anthropic e Gemini permanecem estruturados, porém não fazem parte do provider operacional ativo atual.

k_runtime/

Execution Runtime responsável pela execução controlada dos projetos gerados.

Inclui a CommandPolicy, responsável por validar e controlar comandos permitidos.

A execução de subprocessos utiliza argumentos estruturados e shell=False.

l_validation/

Responsável pelo Validation Gate.

Verifica estrutura e evidências de execução antes de permitir a continuidade do projeto.

m_quality/

Contém o Quality Engine e as verificações relacionadas a qualidade, testes, segurança e dependências.

n_certification/

Responsável pela certificação final e consolidação dos gates obrigatórios.

o_orchestration/

Coordena o Golden Path completo.

Também contém o Repair Loop utilizado quando uma falha recuperável precisa ser corrigida e revalidada.

6. Entrada de Dados

A pasta:

b_input/

contém datasets utilizados como entrada para os projetos.

Entre os datasets presentes no projeto está:

c_dados_vendas.csv

Quando um dataset é fornecido ao workflow, o Dataset Profiling pode analisar fisicamente seu conteúdo antes da definição da arquitetura.

7. Testes

A pasta:

c_tests/

centraliza a estratégia de testes da plataforma, incluindo testes unitários, integração, validação e cenários end-to-end.

8. Documentação

A documentação está organizada em duas perspectivas:

d_documentation/
├── a_documentation_functional/
└── b_documentation_technical/
Documentação Funcional

Explica o que acontece durante o Golden Path, seguindo sua ordem funcional:

AAF
Discovery
Dataset Profiling
Brain
Architecture
Planner
Project Factory
Agents
Skills
MCPs
LLM Gateway
Artifact
Materializer
Generated Projects
Runtime
Validation
Repair Loop
Quality
Certification
Project Ready
Documentação Técnica

Explica como a plataforma é implementada, incluindo:

arquitetura;
operação;
Brain;
Skills;
MCPs;
Agents;
LLM Provider;
CommandPolicy;
Runtime;
Validation;
Quality e Certification;
Obsidian;
apresentação da arquitetura.
9. Brain e Obsidian

Brain e Obsidian possuem responsabilidades diferentes.

Brain

O Brain é operacional.

Ele fornece ao AAF:

contexto;
regras;
padrões;
domínios;
decisões;
relações de conhecimento.
Obsidian

O Obsidian é uma camada de visualização e navegação voltada para pessoas.

O Graph View permite visualizar relações entre conceitos como:

AAF
├── Brain
├── Discovery
├── Architecture
├── Planner
├── Agents
├── Skills
├── MCPs
├── Runtime
├── Validation
├── Quality
└── Certification

Em resumo:

Brain ajuda o AAF a trabalhar com conhecimento e contexto.
Obsidian ajuda uma pessoa a visualizar e navegar por esse conhecimento.

O Obsidian não é uma dependência de execução do Golden Path.

10. Projetos Gerados

Os projetos materializados pelo AAF ficam em:

e_generated_projects/

Cada projeto utiliza seu próprio diretório:

e_generated_projects/<project_id>/

Essa separação permite que o projeto gerado seja executado e analisado de forma independente da implementação interna da plataforma.

11. Exemplo — ETL e Analytics de Vendas

O repositório contém um exemplo simples de projeto de ETL e Analytics:

e_generated_projects/vendas_analytics/
├── README.md
├── requirements.txt
├── pipeline.py
├── test_pipeline.py
├── vendas.db
└── resumo_vendas_por_categoria.csv

A fonte utilizada é:

b_input/c_dados_vendas.csv

O projeto demonstra o seguinte fluxo:

c_dados_vendas.csv
        ↓
      Pandas
        ↓
Limpeza / Transformação
        ↓
      SQLite
        ↓
   tabela vendas
        ↓
       SQL
        ↓
    Analytics
        ↓
resumo_vendas_por_categoria.csv
Transformações

O pipeline:

lê o CSV;
remove * dos campos necessários;
converte datas;
converte valores numéricos;
valida IDs;
remove duplicidades;
carrega os registros tratados no SQLite.
Analytics

Depois da carga, uma consulta SQL calcula:

quantidade de vendas por categoria;
faturamento total por categoria.

O resultado é exportado para:

resumo_vendas_por_categoria.csv
Executando o exemplo

Entre no projeto:

cd e_generated_projects/vendas_analytics

Crie e ative um ambiente virtual, caso necessário:

python3 -m venv venv
source venv/bin/activate

Instale as dependências:

python3 -m pip install -r requirements.txt

Execute:

python3 pipeline.py

O fluxo demonstrado é:

CSV → Pandas/ETL → SQLite → SQL → Analytics → CSV

Para executar os testes do projeto:

python3 -m pytest test_pipeline.py -v
12. CLI do AAF

O ponto de entrada está em:

f_cli/a_main.py

A CLI disponibiliza operações relacionadas a:

aaf start
aaf status
aaf result
aaf brain
aaf mcp

O aaf start inicia o fluxo de geração.

Quando o Discovery precisa de uma informação que realmente altera o projeto, a sessão pode entrar em estado de pausa e posteriormente ser retomada.

13. Session State

A plataforma diferencia dois conceitos de Runtime.

Execution Runtime
a_platform/k_runtime/

Responsável por executar os comandos dos projetos gerados.

Session Runtime State
h_runtime/state/

Responsável por persistir o estado operacional das sessões do próprio AAF.

Essa separação permite cenários como:

Discovery
   ↓
NEEDS_INPUT
   ↓
PAUSED
   ↓
h_runtime/state/
   ↓
Resposta do usuário
   ↓
RESUME
14. Guardrails

O AAF possui diferentes mecanismos de controle ao longo do fluxo.

Entre eles:

contratos tipados;
validação de Agents;
Skill Registry;
MCP Registry;
validação de domínio;
CommandPolicy;
PathPolicy;
Validation Gate;
Quality Engine;
Certification Engine;
evidências tipadas de execução.

O objetivo é evitar que uma simples geração de arquivos seja interpretada como evidência de que um projeto está pronto.

15. Limitações Atuais

O projeto possui algumas limitações explicitamente reconhecidas:

o Golden Path é especializado em Analytics e Data Engineering;
OpenAI é o provider operacional ativo do LLM Gateway;
Anthropic e Gemini não fazem parte do fluxo operacional ativo atual;
o Learning Engine está fora do Golden Path;
a IDE atua como interface/transporte, enquanto o raciocínio da fábrica pertence aos componentes internos do AAF;
a existência de um projeto materializado não significa automaticamente que todo o Golden Path E2E do AAF foi homologado.
16. Definition of Ready

Um projeto está pronto para entrar no processo de geração quando:

os requisitos necessários foram compreendidos;
o contexto relevante foi identificado;
datasets disponíveis foram analisados quando aplicável;
o Brain Context está disponível para arquitetura e planejamento.
17. Definition of Done

O objetivo final do Golden Path é atingir:

Discovery        COMPLETE
Planning         COMPLETE
Materialization  SUCCESS
Execution        SUCCESS
Validation       PASS
Quality          PASS
Certification    PASS

Somente com todos os gates aprovados:

PROJECT READY = YES
18. Resumo

O Analytics Agents Factory organiza a geração de projetos através de responsabilidades especializadas:

Brain          → conhecimento, contexto e regras
Agents         → especialistas
Skills         → capacidades
MCPs           → acesso controlado a recursos
LLM Gateway    → inteligência generativa
ProjectFactory → coordenação da geração
Materializer   → criação dos arquivos
Runtime        → execução
Validation     → validação
Repair Loop    → recuperação de falhas
Quality        → evidências de qualidade
Certification  → decisão final

O AAF transforma:

Intenção humana
      ↓
Contexto
      ↓
Arquitetura
      ↓
Plano
      ↓
Agents + Skills + MCPs + LLM
      ↓
Projeto
      ↓
Execução
      ↓
Validação
      ↓
Qualidade
      ↓
Certificação

O AAF não é apenas um Agent que gera código: é uma fábrica multiagente de projetos de Analytics e Data Engineering projetada para transformar uma intenção em uma implementação estruturada, executável e validável.


Essa versão também incorpora o **`vendas_analytics` como demonstração prática**, o que ajuda bastante quem abrir o GitHub depois da apresentação: a pessoa consegue entender o AAF conceitualmente e logo depois executar um exemplo pequeno.