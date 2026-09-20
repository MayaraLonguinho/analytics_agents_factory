# Segurança e Guardrails (Security & Guardrails)

> **Documentação Técnica Oficial — Políticas de Isolamento, Sandbox e Integridade Operacional**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[j_repair_orchestration|Anterior: Orquestração de Reparo]] | [[l_testing_strategy|Próximo: Estratégia de Testes]]

---

## 1. Visão Geral de Segurança no AAF

A arquitetura do Analytics Agents Factory é projetada sob o princípio de **Defesa em Profundidade (Defense in Depth)**. Como a plataforma coordena agentes de inteligência artificial autônomos com capacidade de gerar e executar código real em sistemas operacionais, múltiplas camadas de restrição e isolamento foram estabelecidas para impedir vulnerabilidades, vazamento de dados ou execuções destrutivas.

---

## 2. A Política de Caminhos (`PathPolicy`)

A `PathPolicy` (`a_platform/i_materializer/b_path_policy.py`) atua como sandbox do sistema de arquivos para toda a persistência realizada pela fábrica:

1. **Restrição Absoluta de Escrita:** Toda operação física de criação de arquivo é restrita ao subdiretório exclusivo do projeto:
   ```text
   e_generated_projects/<project_id>/
   ```
2. **Prevenção de Path Traversal:** Rejeição de caminhos que contenham sequências de escape (`../`, `..\\`), links simbólicos circulares ou caracteres de controle;
3. **Validação de Canonicidade:** O caminho real absoluto (`os.path.realpath`) é resolvido e testado compulsoriamente contra o prefixo da pasta do projeto. Se não houver correspondência exata, a operação lança `PathPolicyViolationError` e é abortada.

---

## 3. A Política de Comandos (`CommandPolicy`)

A `CommandPolicy` (`a_platform/k_runtime/b_command_policy/a_policy.py`) governa a execução de processos pelo Runtime:

1. **Preflight no Planejamento:** O `PlannerAgent` valida preventivamente todos os comandos propostos;
2. **Enforcement no Runtime:** O `RuntimeEngine` impede o disparo de comandos fora da política;
3. **Whitelist Rígida de Binários:** Apenas executáveis analíticos homologados são autorizados (`python`, `pytest`, `pip`, `flake8`, `ruff`, `bandit`);
4. **Execução sem Shell (`shell=False`):** Proibição total de uso de shells intermediários, eliminando riscos de injeção de comandos;
5. **Bloqueio de Encadeamento:** Operadores de terminal como `&&`, `||`, `;`, `|`, `>`, `<` são terminantemente bloqueados.

---

## 4. Fronteiras de MCPs e LLM Gateway

A plataforma estabelece barreiras rígidas para ferramentas e inteligência:

- **Fronteiras de MCP (Model Context Protocol):**
  - O `Filesystem MCP` obedece à `PathPolicy`;
  - O `Database MCP` bloqueia comandos de manipulação externa (`ATTACH`, `DETACH`) e restringe o acesso a bancos locais SQLite/DuckDB do projeto;
  - O `Docker MCP` opera sob whitelist restrita de subcomandos (`build`, `run`, `ps`, `logs`, `stop`, `rm`), sem interpolação de strings.
- **Fronteiras do LLM Gateway:**
  - Proibição absoluta de importação de SDKs externos (`openai`, `anthropic`, etc.) fora do Gateway;
  - Centralização de timeouts, retries e sanitização de prompts e saídas.

---

## 5. Gestão de Segredos e Variáveis de Ambiente (`.env`)

1. **Isolamento de Credenciais:** Nenhuma chave de API, senha de banco de dados ou token de serviço é commitado no repositório ou exposto em código-fonte;
2. **Uso de `.env`:** As credenciais operacionais (como `OPENAI_API_KEY`) residem exclusivamente no arquivo `.env` local (ignorado pelo `.gitignore`), sendo carregadas via `g_configuration/a_settings.py`;
3. **Sanitização de Logs:** Logs de auditoria, laudos de gates e saídas de terminal são higienizados para prevenir o vazamento acidental de tokens em `stdout` ou `stderr`.

---

## 6. As Três Proibições Conceituais Absolutas

Para manter a integridade da engenharia da plataforma, três práticas são categoricamente proibidas:

### 6.1 Proibição de Sucesso Artificial (`No Fake Success`)
É terminantemente proibido forjar laudos, emular aprovações ou simular execuções através de mocks para mascarar falhas reais do pipeline. Sucesso só existe quando comprovado por evidências físicas (exit code 0, arquivos gerados, testes passando).

### 6.2 Proibição de Fallback Silencioso (`No Silent Fallback`)
É proibido capturar exceções silenciosamente (`except: pass`) transformando erros em status positivo sem diagnóstico. Toda falha deve ser propagada ou enviada ao ciclo formal de reparo.

### 6.3 Proibição de Invenção de Regras de Negócio (`No Invented Rules`)
O AAF é estritamente agnóstico ao domínio do usuário. É proibido inferir premissas de negócio que não constem na solicitação ou no dataset fornecido. Se uma decisão for necessária, aciona-se o protocolo `NEEDS_INPUT`.

---

## 7. Target Contract vs. Current Implementation Status

- **Target Contract:** Auditoria contínua de segurança com sandbox em namespace Linux/Docker e verificação automática de segredos via pre-commit hooks nativos da plataforma.
- **Current Implementation Status:** A `PathPolicy`, a `CommandPolicy` com preflight e enforcement, o isolamento do `LLMGateway` e as restrições de sandbox em `f_mcps/` estão ativas e implementadas no código.

---

## Navegação

- Documento anterior: [[j_repair_orchestration|Orquestração de Reparo]]
- Próximo passo técnico: [[l_testing_strategy|Estratégia de Testes]]
- Contrato da IDE: [[a_system_architecture|Arquitetura do Sistema]]
