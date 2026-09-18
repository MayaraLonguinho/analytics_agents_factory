# Model Context Protocol (MCP)

Os `MCPs` representam a única via de contato da plataforma com o sistema operacional local. A Fábrica não roda comandos `os.system` livremente durante a produção de artefatos. Tudo deve passar por `f_mcp`.

## MCPs Implementados

### 1. Filesystem MCP
- **Responsabilidade**: Ler e escrever em disco.
- **Segurança (Sandbox)**: Limite arquitetural rigoroso ao destino. O Filesystem é interceptado na função `is_safe_path(full_path)`, que reverte e bloqueia acesso de gravação fora da pasta permitida: `e_generated_projects/`. Modificação transversal de pastas alheias ao escopo gerado atirará falha operacional no Pipeline de Geração.

### 2. Database MCP
- **Responsabilidade**: Inicializar dados, provar testes unitários SQL através da simulação na infraestrutura SQLite local gerada.
- **Segurança**: Previne execuções maliciosas. Regras estritas barram comandos de `ATTACH` e `DETACH`, prevenindo vazamento de dados de bancos externos não autorizados, e restringem certas diretivas na função `is_safe_query(query)`.

### 3. Docker MCP
- **Responsabilidade**: Orquestrar containers do pipeline da Factory (usualmente durante a fase de Runtime ou Quality para rodar os testes da suíte em container gerado).
- **Segurança**: 
  - Subcomandos suportados via Whitelist limitados a: `ps`, `run`, `logs` e `build`.
  - O MCP de Docker intercepta o comando usando o array `shlex.split`, removendo absolutamente a capacidade de instigar vulnerabilidades baseadas no escape nativo de bash (`shell=True` removido com severidade total do ambiente). 

## Executor e Limites
Todas as chamadas invocam a fachada centralizada em `e_executor/a_executor.py` (`MCPExecutor`). Limites de escopo garantem a imunidade da Plataforma, mesmo diante de eventuais viesses perversos injetados pelo Agente / LLM. Qualquer erro não sanado no contexto restrito é escalado via diagnostico, reprovando o *readiness* geral.
