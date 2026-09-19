# Uso Operacional da Plataforma (Operational Use)

> **Documentação Funcional Oficial — Comandos da CLI, Sessões e Operação**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[i_project_ready_and_delivery|Anterior: Project Ready e Entrega]] | [[a_system_architecture|Início Técnico: Arquitetura do Sistema]]

---

## 1. Ponto de Entrada Oficial: CLI da Plataforma

O AAF é operado através de sua interface de linha de comando oficial localizada em `f_cli/a_main.py` (ou através do comando de alias `aaf` quando instalado no ambiente):

```bash
python f_cli/a_main.py <comando> [opções]
```

A interface CLI garante que qualquer usuário, pipeline de CI/CD ou agente de IDE possa interagir com a fábrica de forma idempotente, segura e governada.

---

## 2. Comandos Oficiais da CLI

A plataforma suporta estritamente os seguintes comandos (não execute ou presuma comandos inexistentes):

### 2.1 `start`: Inicializar ou Retomar um Projeto
Inicia a fabricação de um novo projeto analítico ou responde a uma pendência de Discovery em uma sessão pausada.

- **Iniciar novo projeto com prompt e dataset:**
  ```bash
  python f_cli/a_main.py start --project-id "vendas_analytics" --prompt "Criar pipeline ETL para ler dados brutos de vendas, tratar valores nulos e carregar em banco analítico SQLite com testes pytest" --dataset "./b_input/dados_vendas.csv"
  ```
- **Retomar uma sessão pausada (`NEEDS_INPUT`) com a resposta do usuário:**
  ```bash
  python f_cli/a_main.py start --project-id "vendas_analytics" --answer "Utilize a granularidade diária e armazene na tabela fato_vendas_diaria"
  ```

### 2.2 `status`: Consultar o Estado da Sessão
Permite acompanhar o estado corrente da máquina de estados de um projeto em execução, pausado ou finalizado.

```bash
python f_cli/a_main.py status vendas_analytics
```
*Saída típica:*
- Identificador do projeto (`project_id`);
- Status da máquina de estados (`INITIALIZED`, `DISCOVERY`, `NEEDS_INPUT`, `GENERATING`, `READY`, `FAILED`);
- Pergunta pendente (caso esteja em `NEEDS_INPUT`);
- Timestamp da última atualização.

### 2.3 `result`: Recuperar o Laudo e Resumo da Entrega
Exibe as evidências consolidadas de um projeto que concluiu a fabricação.

```bash
python f_cli/a_main.py result vendas_analytics
```
*Saída típica:*
- Veredito final (`PROJECT READY = YES` ou `NO`);
- Caminho absoluto do projeto gerado em `e_generated_projects/<project_id>/`;
- Lista de arquivos materializados;
- Resumo dos laudos de validação, qualidade e certificação.

### 2.4 `brain`: Inspecionar Conhecimento e Regras
Exibe os domínios configurados, padrões cadastrados e decisões ativas no subsistema Brain.

```bash
python f_cli/a_main.py brain
```

### 2.5 `mcp`: Inspecionar Ferramentas e Protocolos MCP
Lista os MCPs operacionais registrados na fábrica e seus status de disponibilidade.

```bash
python f_cli/a_main.py mcp
```

---

## 3. Gerenciamento de Estado de Sessão (`Session State`)

A persistência do ciclo de vida da fábrica é governada pelo `StateManager` (`a_platform/b_contracts/j_state_manager.py`):
- **Localização dos Checkpoints:**  
  Todos os estados são salvos em arquivos JSON dedicados sob:
  ```text
  h_runtime/state/<project_id>.json
  ```
- **Estrutura do Checkpoint:**  
  Contém metadados da sessão, histórico de Discovery, premissas (`assumptions`), decisões arquiteturais, progresso das tarefas e perguntas pendentes.
- **Idempotência:**  
  A fábrica nunca perde o progresso já validado caso o processo seja interrompido. Ao retomar a execução com o mesmo `project_id`, o estado é reidratado a partir do último checkpoint íntegro.

---

## 4. O Ciclo de Pausa e Retomada (`Pause & Resume`)

O ciclo operacional entre o usuário e o `DiscoveryAgent` ocorre de forma fluida:

1. **Disparo Inicial:** O usuário executa `aaf start` com um objetivo complexo;
2. **Identificação de Dúvida Indispensável:** O `DiscoveryAgent` identifica que um critério central depende de escolha humana;
3. **Pausa Segura:** O orquestrador salva o estado em `h_runtime/state/<project_id>.json` com status `NEEDS_INPUT`, imprime a pergunta única e encerra o processo com código de pausa limpo;
4. **Interação com Usuário:** O usuário visualiza a pergunta em seu terminal ou na interface de chat da IDE;
5. **Retomada:** O usuário submete a resposta executando `aaf start --project-id <id> --answer "<resposta>"`;
6. **Descongelamento:** O AAF recarrega o contexto, valida a resposta e dá prosseguimento imediato ao Golden Path.

---

## 5. Onde os Projetos Gerados Aparecem

Ao alcançar o encerramento com sucesso (`PROJECT READY = YES`), a aplicação final gerada está localizada em:

```text
e_generated_projects/<project_id>/
```

O usuário pode navegar até a pasta, ativar um ambiente virtual local, instalar os `requirements.txt` gerados e executar os comandos indicados no `README.md` do projeto com total reprodutibilidade.

---

## 6. Target Contract vs. Current Implementation Status

- **Target Contract:** CLI unificada com subcomandos avançados de streaming de telemetria, cancelamento de sessão gracioso e empacotamento zip/tarball para exportação direta.
- **Current Implementation Status:** Os comandos essenciais `start` (com suporte a prompt, dataset e answer), `status`, `result`, `brain` e `mcp` estão plenamente implementados em `f_cli/a_main.py` e integrados ao `StateManager`.

---

## Navegação

- Documento anterior: [[i_project_ready_and_delivery|Project Ready e Entrega]]
- Próximo passo (Arquitetura Técnica): [[a_system_architecture|Arquitetura do Sistema]]
