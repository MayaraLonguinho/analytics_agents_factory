# Brain (SSOT - Single Source of Truth)

O `Brain` é o coração cognitivo e normativo da Analytics Agents Factory. Ele não é apenas um repositório de RAG, é a única fonte da verdade arquitetural (SSOT) para os Agentes tomarem decisão durante o plano e implementação de código.

## Conhecimento (`a_knowledge/`)
Arquivos Markdown contendo o detalhamento de domínios (ex: `a_platform.md`, `b_data_engineering.md`, `c_analytics.md`).
- Estes arquivos ensinam o LLM sobre o "o que" é cada domínio, melhores práticas de mercado e paradigmas adotados pelo sistema.

## Regras (`b_rules/`)
Diretivas operacionais fortes:
- `c_architecture_rules.md`: Regras imutáveis de design (Design Patterns exigidos, exclusão estrita de microserviços etc).
- `d_data_rules.md`: Modelagem esperada, *Naming Conventions* de tabelas e diretrizes de integridade.
- `e_sql_rules.md`: Instruções sobre dialetos SQL, CTEs compulsórias e performance de consultas.
- `f_testing_rules.md`: Estrutura base para suítes `pytest`.
- `g_documentation_rules.md`: Templates de Readmes.
- `h_project_ready_rules.md`: Limites severos de Gates (o que constitui estar Pronto).

## Memória, Contexto e Decisões
- O `c_brain` gerencia de forma centralizada os registros através dos seus `Registries` (Knowledge, Pattern e Rule).
- `d_decisions/a_decision_store.py`: Guarda decisões passadas dentro do log de memória do projeto para que refatorações subsequentes compreendam por que uma determinada biblioteca foi escolhida ou por que uma tabela SQL usa certa restrição.

## Relação com o Graph
Embora haja integração baseada em grafos do Obsidian (`.obsidian/`), o Graph **não é o SSOT** (Single Source of Truth) e não contém regras de lógica da plataforma. O Graph atua como visualização de rede, mas a verdade emana puramente da estrutura em disco legível do Brain.
