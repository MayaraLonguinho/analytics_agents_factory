# Analytics Agents Factory (AAF)

## Objetivo
A **Analytics Agents Factory (AAF)** é uma fábrica de software operada por agentes autônomos especializados na construção de pipelines de **Analytics e ETL/ELT**. Ela foi concebida de forma completamente **agnóstica ao domínio de negócio**, sendo capaz de modelar bases, transformar dados e expor indicadores sem engessamento conceitual. (A geração de projetos de *Personal Finance*, por exemplo, é uma mera capacidade opcional e não o domínio exclusivo do núcleo).

## Arquitetura
A plataforma opera sob um padrão de **Modular Monolith**. Todos os serviços, *agents*, *skills* e orquestrações pertencem ao mesmo repositório e contexto, o que simplifica o estado, validação e governança, rejeitando a complexidade indevida de microserviços.

## Fluxo Operacional
O ciclo de vida da geração de um projeto respeita rigorosamente as seguintes etapas:
`IDE Chat` → `IDE Adapter` → `Discovery` → `Dataset Profiling` → `Brain` → `Architecture` → `Planner` → `Project Factory` → `Agents + Skills + MCPs + LLM Gateway` → `Artifact Materializer` → `e_generated_projects/` → `Execution Runtime` → `Validation Gate` → `Repair Loop` → `Quality Engine` → `Certification Engine` → **PROJECT READY**.

O AAF não gera meramente "arquivos de texto"; ele de fato os materializa, executa na engine, valida, avalia a estrutura via testes, repara bugs através do *Repair Loop* (caso os *Gates* não passem) e só então certifica a prontidão do projeto.

## Estruturas Principais

### Agentes Principais
Os agentes lidam com especialidades autônomas, comunicando-se com o *Brain* e sendo guiados pelo *Planner*.
- **Agent Factory:** Fábrica responsável pela inicialização.
- **Planner Agent:** Gera e rastreia planos de execução.
- **Discovery Agent:** Entende a necessidade e faz profiling.
- **Data & Analytics Agents:** Escrevem lógicas de transformação e cálculo.
- Outros: Testing, Documentation, Database, Backend, Frontend, Chatbot, Infrastructure e Base Agents.

### Skills
Capacidades determinísticas e injetáveis fornecidas aos agentes.

### MCPs (Model Context Protocol)
Integrações seguras utilizadas:
- **Filesystem MCP**: Leitura, listagem e escrita segura.
- **Database MCP**: Manipulação de *engines* suportadas (ex: SQLite).
- **Docker MCP**: Informações de containerização e isolamento.

*(Aviso: Integrações de Git MCP não fazem parte do escopo da plataforma).*

### LLM Gateway
Acesso unificado abstraindo provedores (sem lógicas acopladas diretamente no agente):
- **OpenAI**
- **Gemini**
- **Anthropic**

*(Aviso: Ollama ou LLMs locais não integram a stack).*

### Brain & Graph (Obsidian)
- **Brain**: O repositório central de inteligência da plataforma, contendo restrições operacionais e conhecimento (`c_brain/`).
- **Graph/Obsidian**: Utilizado puramente como camada visual representativa, sem a construção de aplicações gráficas acopladas.

## Como Executar (CLI Oficial)
A execução interativa da fábrica, testes e checagem de orquestração se dão através do entrypoint da CLI (construído em Python). **Não utilize Continue IDE ou outras ferramentas externas para emular a orquestração. O Git também não faz parte da operação do agente nem da fábrica.**

Para interagir com o ecossistema localmente, os **comandos canônicos** são:
- Iniciar uma fábrica (requisição interativa):
  ```bash
  python -m a_platform.b_interfaces.b_cli.b_cli start
  ```
- Obter status:
  ```bash
  python -m a_platform.b_interfaces.b_cli.b_cli status <project_id>
  ```
- Ver os resultados e artefatos de um projeto finalizado:
  ```bash
  python -m a_platform.b_interfaces.b_cli.b_cli result <project_id>
  ```
- Executar os testes estáticos de MCPs:
  ```bash
  python -m a_platform.b_interfaces.b_cli.b_cli mcp
  ```
- Despejar conhecimento carregado do Brain:
  ```bash
  python -m a_platform.b_interfaces.b_cli.b_cli brain
  ```

*(Para rodar via docker, utilize: `docker-compose run aaf python -m a_platform.b_interfaces.b_cli.b_cli <comando>`)*

## Golden Paths & Qualidade

Para que a plataforma considere um **PROJECT READY**, as premissas são inflexíveis:
- **Discovery** = `COMPLETE`
- **Planning** = `COMPLETE`
- **Materialization** = `SUCCESS`
- **Execution** = `SUCCESS`
- **Validation** = `PASS`
- **Quality** = `PASS`
- **Certification** = `PASS`

**Regra Dourada:** A ausência de evidência estrutural ou erro de testes significa **falha** (`PASS = FALSE`). Projetos gerados devem obrigatoriamente ser executáveis e comprovados pela plataforma. Projetos gerados são persistidos dentro da pasta `e_generated_projects/`.

---
*Referência Conceitual Arquitetural: [ai-project-pipeline](https://github.com/gustavomot4/ai-project-pipeline)*
