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
- **c_brain**: A máquina de políticas e Retrieval (força regras sem árbitrio).
- **g_agents / e_skills / f_mcps**: Os cérebros ativos (Agentes) utilizando Skills e executando MCPs de Filesystem/Database/Docker isolados e políticos.
- **h_factory / h_materializer**: Responsáveis estritos pela coordenação e IO do código final.
- **j_runtime / k_validation / l_quality / m_certification**: O portão rigoroso de qualidade.

## 4. O Fluxo de Geração
1. **Discovery**: Identificação das intenções e dataset.
2. **Brain & Planner**: Design de arquitetura e divisão de tarefas.
3. **Factory & Agents**: Gula e construção de *Artifacts*.
4. **Materializer**: Gravação *Capability-based* no disco na pasta protegida `e_generated_projects`.
5. **Runtime**: Subprocessos físicos, gravando *stdout* e *stderr*.
6. **Validation & Quality**: Validação da base das evidências geradas. 
7. **Certification**: `PROJECT READY = YES` apenas se tudo retornar êxito total.

## 5. Como Iniciar
Crie seu ambiente e ative:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Preencha o `.env` (via `.env.example`).

## 6. Comandos CLI (f_cli/a_main.py)
A CLI expõe a complexidade subjacente sem mimetizá-la:
- `python f_cli/a_main.py start --project-id <id> --prompt "<prompt>"`: Inicia o gerador.
- `python f_cli/a_main.py status <project_id>`: Traz a situação atual do pipeline.
- `python f_cli/a_main.py result <project_id>`: Confirmação de entrega (`READY`).
- `python f_cli/a_main.py brain`: Sumário de regras canônicas operacionais.
- `python f_cli/a_main.py mcp`: Lista de integradores físicos rodando no sistema.

## 7. LLM Providers
Apenas a biblioteca `openai` está funcional e configurada para operar via `i_llm_gateway`. (Gemini e Anthropic disparam abertamente erros de sistema).

## 8. Limitações e Honestidade Técnica
O projeto prioriza a infraestrutura de controle, logo:
- Processos de testes End-to-End estão momentaneamente silenciados (`NÃO execute testes`).
- O ecossistema de *repair_loop* foi solidificado logicamente para intervir caso haja *FAIL*, e está ciente e aderente aos metadados.
- Não há frameworks complexos para a CLI, rodando inteiramente sobre `argparse`.
