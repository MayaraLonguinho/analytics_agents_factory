# Analytics Agents Factory (AAF)

## 1. O que é o AAF?
O **Analytics Agents Factory** é uma fábrica de software gerado baseada em inteligência artificial. 
É especializado **exclusivamente** nos domínios de Analytics e Engenharia de Dados (ETL/ELT). Ele materializa, executa e valida projetos reais a partir de prompts em linguagem natural.

## 2. Escopo
- **Domínios**: Analytics, Data Engineering.
- **Capabilities Opcionais**: Frontend, Backend, Dashboarding.
- **Saída**: Monolitos modulares altamente coerentes e orientados a testes.

## 3. Arquitetura
O AAF opera sem *mocks* e sem falsos positivos, empregando o paradigma *Absence of Evidence = Failure*.
Sua árvore de módulos inclui:
- **b_contracts**: Contratos canônicos (Artifact, ProjectPlan, ExecutionContext).
- **c_brain**: A máquina de políticas e Retrieval (força regras sem arbítrio).
- **g_agents / e_skills / f_mcps**: Os cérebros ativos (Agentes) utilizando Skills e executando MCPs de Filesystem/Database/Docker isolados e políticos.
- **h_factory / h_materializer**: Responsáveis estritos pela coordenação e IO do código final na pasta segura.
- **j_runtime / k_validation / l_quality / m_certification**: O portão rigoroso de qualidade, exigindo provas operacionais no disco e da análise de código estruturada.

## 4. O Fluxo de Geração
1. **Discovery**: Identificação das intenções e dataset.
2. **Brain & Planner**: Design de arquitetura e divisão topológica de tarefas.
3. **Factory & Agents**: Geração baseada no grafo de dependência dos *Artifacts*.
4. **Materializer**: Gravação estruturada e protegida em `e_generated_projects`.
5. **Runtime**: Execução através de Subprocessos com `shell=False` estrito, gravando *stdout* e *stderr* e bloqueando comandos destrutivos.
6. **Validation & Quality**: Validação baseada em evidências físicas e resultados do runtime. O `Repair Loop` atua reativando o Agente caso exista falha na execução.
7. **Certification**: `PROJECT READY = YES` apenas se tudo retornar êxito total, sem exceções.

## 5. Como Iniciar
Crie seu ambiente e ative:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Preencha o `.env` copiando a partir de `.env.example`.

## 6. Comandos CLI
A CLI oficial `aaf` expõe a complexidade subjacente (lembre-se de rodar dentro do ambiente virtual):
- `aaf start --project-id <id> --prompt "<prompt>"`: Inicia o gerador.
- `aaf status <project_id>`: Traz a situação atual do pipeline e fases concluídas.
- `aaf result <project_id>`: Confirmação de entrega oficial do projeto (`READY`).
- `aaf brain`: Sumário de regras canônicas e de conformidade do Brain.
- `aaf mcp`: Lista de ferramentas MCP ativadas no sistema.

## 7. LLM Providers
Apenas a interface conectada à biblioteca `openai` está em modo ativo e configurada para operar via `i_llm_gateway`.

## 8. Limitações e Honestidade Técnica
O projeto prioriza infraestrutura de controle:
- Processos de testes End-to-End não são disparados automaticamente pelo pipeline sem permissão (regra `NÃO execute testes`).
- O ecossistema do *Repair Loop* opera com limite fixo (3 tentativas) e intervém relançando a tarefa para a inteligência responsável analisar o log.
