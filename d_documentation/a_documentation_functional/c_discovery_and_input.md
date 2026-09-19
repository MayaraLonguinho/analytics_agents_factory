
# Discovery e Entrada de Dados (Input Protocol)

> **Documentação Funcional Oficial — Elicitação de Requisitos e Profiling**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[b_golden_path|Anterior: Golden Path]] | [[d_planning_and_decomposition|Próximo: Planejamento e Decomposição]]

---

## 1. Canais de Entrada e Linguagem Natural

A plataforma AAF é acionada primariamente por solicitações em linguagem natural, permitindo que usuários de diferentes níveis de senioridade expressem suas necessidades analíticas:

1. **CLI Oficial (`f_cli/a_main.py` ou `aaf`):**
   ```bash
   python f_cli/a_main.py start --project-id "vendas_etl" --prompt "Criar pipeline de ingestão CSV de vendas, sanitizar nulos, agregar por região e salvar em SQLite com testes" --dataset "./b_input/dados_vendas.csv"
   ```
2. **IDE Chat / Adapter:**  
   Em ambientes integrados (IDE Antigravity, editores assistidos por IA), o chat atua estritamente como **camada de transporte e interface**. O agente da IDE repassa o comando ao `IDEAdapter`, sem executar o Discovery por conta própria nem inventar requisitos.

---

## 2. O Papel do DiscoveryAgent

O `DiscoveryAgent` (`a_platform/g_agents/b_discovery/`) tem como missão transformar um texto livre do usuário em requisitos estruturados, livres de ambiguidade e alinhados à capacidade técnica da fábrica:

1. **Extração de Domínio Técnico:** Mapeia o objetivo principal em um dos domínios da plataforma (`analytics` ou `data_engineering`);
2. **Identificação de Objetivos:** Isola fontes de entrada, transformações pretendidas, métricas chave e formatos de persistência desejados;
3. **Avaliação de Completude:** Checa se o projeto possui escopo suficiente para ser arquitetado e planejado sem suposições perigosas.

---

## 3. Protocolo Estrito de Discovery

Para evitar interrogatórios intermináveis ou fricção excessiva com o usuário, o Discovery obedece a regras inegociáveis:

1. **Teto Máximo de 5 Perguntas:** Em nenhuma hipótese o `DiscoveryAgent` fará mais do que 5 perguntas em toda a sessão do projeto.
2. **Uma Pergunta por Vez (`One Question at a Time`):** É terminantemente proibido enviar listas ou blocos com múltiplas perguntas simultâneas.
3. **Critérios Estritos para Perguntar:** Uma pergunta **só é autorizada** se sua resposta alterar diretamente:
   - A arquitetura técnica da solução;
   - O escopo ou limites do projeto;
   - Uma *Capability* indispensável a ser executada;
   - A fonte dos dados (`source`) ou destino de persistência (`target`);
   - Os critérios de aceitação e validação;
   - Uma decisão técnica essencial sem alternativa viável.
4. **Premissas Técnicas Explícitas (`Assumptions`):** Detalhes secundários, convenções de código, nomenclaturas padrão e incertezas menores **não devem** gerar perguntas. Devem ser convertidos em premissas explícitas registradas no Brain.
5. **Registro de Decisões Não Resolvidas (`Q-NN`):** Questões pendentes ou pontos de refinamento futuro são catalogados como `Q-01`, `Q-02`, etc., permitindo rastreabilidade sem bloquear a esteira.

---

## 4. O Mecanismo de Pausa e Retomada (`NEEDS_INPUT / PAUSED / RESUME`)

Quando o `DiscoveryAgent` precisa obrigatoriamente de uma resposta humana para prosseguir:

```text
DiscoveryAgent detecta falta de informação crítica
              ↓
Status transiciona para NEEDS_INPUT
              ↓
StateManager grava checkpoint em h_runtime/state/<project_id>.json
              ↓
Orquestrador entra em PAUSED e exibe a pergunta única
              ↓
[Usuário responde via CLI ou Chat]
              ↓
aaf resume / --answer "resposta fornecida"
              ↓
Estado entra em RESUMED
              ↓
Contexto é reidratado no Brain
              ↓
Discovery conclui e libera Dataset Profiling
```

---

## 5. Dataset Profiling: Análise Factual de Dados

Quando a solicitação faz referência a um dataset físico ou o usuário fornece o caminho via `--dataset` (geralmente apontado em `b_input/`):

1. **Inspeção Física Direta:** O `DatasetProfilingSkill` (`a_platform/e_skills/a_dataset_profiling/`) lê o arquivo diretamente em disco usando Pandas/DuckDB;
2. **Extração de Metadados Sem IA:** A extração não usa LLM e não usa mocks; é puramente analítica e estatística:
   - Contagem exata de linhas (`row_count`) e colunas (`column_count`);
   - Lista exata de nomes de colunas;
   - Tipos de dados inferidos por coluna (`dtypes`);
   - Porcentagem de valores nulos e ausentes;
   - Contagem de registros duplicados e cardinalidade;
   - Amostras reais de dados das primeiras linhas;
3. **Consolidação no Brain:** As evidências numéricas e estruturais são salvas no Brain (`request.dataset_profile`), impedindo que agentes futuros alucinem schemas ou nomes de campos inexistentes.

---

## 6. Distinção Crítica: Ausência de Dado vs. Ausência de Decisão

A governança do AAF estabelece uma separação funcional clara:

- **Ausência de Dado (Data Absence):**  
  O usuário quer que o projeto processe um dataset mas não forneceu o arquivo ou apontou um caminho inexistente em disco.  
  *Tratamento:* Não é um problema conceitual de requisitos; o sistema alerta a ausência do arquivo físico no path especificado. Se o projeto for um gerador autônomo com criação de schema, datasets sintéticos homologados podem ser gerados pelos agentes da fábrica.
- **Ausência de Decisão (Decision Absence):**  
  O usuário forneceu os dados, mas o objetivo ou critério de transformação é ambíguo (ex: "calcule o score de clientes", sem especificar quais variáveis ou regras definem o score).  
  *Tratamento:* Se puder ser inferido com base nas convenções de domínio do Brain, cria-se uma `assumption`. Se for indispensável e alterar a arquitetura ou métrica central, dispara-se uma pergunta sob o protocolo `NEEDS_INPUT → PAUSED`.

---

## 7. Target Contract vs. Current Implementation Status

- **Target Contract:** O `DiscoveryAgent` gerencia o teto de 5 perguntas de forma totalmente interativa através de qualquer interface (CLI, API ou IDE), garantindo que após a resolução de `Q-NN` ou respostas de `NEEDS_INPUT`, o fluxo retome sem perda de estado. O `DatasetProfiling` atua de forma universal sobre qualquer formato de dados estruturado (CSV, Parquet, JSON, bancos relacionais).
- **Current Implementation Status:** O `DiscoveryAgent` e o `StateManager` implementam o ciclo `NEEDS_INPUT` com persistência em JSON em `h_runtime/state/<project_id>.json`. O `DatasetProfilingSkill` suporta nativamente arquivos CSV e JSON com Pandas. A interação via CLI com `--answer` retoma a sessão adequadamente.

---

## Navegação

- Documento anterior: [[b_golden_path|Golden Path Oficial]]
- Próximo passo funcional: [[d_planning_and_decomposition|Planejamento e Decomposição]]
- Referência técnica: [[c_brain_and_context|Brain e Gestão de Contexto]]
