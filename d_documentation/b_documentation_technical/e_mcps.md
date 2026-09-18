# Model Context Protocol (MCP)

Os `MCPs` (`a_platform/f_mcps`) constituem a única interface autorizada para interação entre a plataforma AAF e recursos do ambiente operacional (disco, banco de dados e containers). Agentes e skills nunca executam comandos `os.system` ou I/O direto sem passar pela camada MCP.

## MCPs Implementados

### 1. Filesystem MCP (`b_filesystem/`)
- **Responsabilidade**: Leitura e escrita de arquivos para persistência e materialização.
- **Segurança (Sandbox Estrito)**: Interceptado pela função `is_safe_path(full_path)`. Qualquer tentativa de escrita fora do diretório de destino permitido (`e_generated_projects/`) é bloqueada e resulta em erro operacional.

### 2. Database MCP (`c_database/`)
- **Responsabilidade**: Execução de scripts DDL/DML para validação e testes em bancos locais SQLite gerados para o projeto.
- **Segurança**: Previne execuções arbitrárias via `is_safe_query(query)`. Comandos como `ATTACH` e `DETACH` são terminantemente bloqueados para evitar vazamento ou contaminação de bases externas.

### 3. Docker MCP (`d_docker/`)
- **Responsabilidade**: Orquestração de containers para execução de testes em ambiente isolado durante as fases de Runtime e Quality.
- **Segurança**:
  - Whitelist restrita de subcomandos permitidos: `ps`, `run`, `logs`, `build`.
  - Argumentos são divididos via `shlex.split`, garantindo a execução via lista de argumentos com `shell=False`. Proibição absoluta de injeção de comandos de shell.

## MCP Executor

Todas as chamadas para as ferramentas MCP passam pela fachada centralizada `MCPExecutor` (`e_executor/a_executor.py`), que centraliza telemetria, captura de erros e auditoria de segurança das operações.
