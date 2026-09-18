# Brain (SSOT - Single Source of Truth)

O `Brain` é o coração cognitivo e normativo da Analytics Agents Factory. Ele não é apenas um repositório de RAG, é a única fonte da verdade arquitetural (SSOT) para os Agentes tomarem decisão durante o plano e implementação de código.

## Domínios e Contexto (`d_domains/`, `a_context/`)
Arquivos Markdown contendo o detalhamento de domínios analíticos (`a_analytics.md`, `b_data_engineering.md`) e contexto operacional.
- Estes arquivos ensinam o LLM sobre as fronteiras canônicas de cada domínio, melhores práticas e paradigmas adotados pelo sistema.

## Regras (`b_rules/`)
Diretivas operacionais fortes:
- `c_architecture_rules.md`: Regras imutáveis de design (Design Patterns exigidos, exclusão estrita de microserviços etc).
- `d_data_rules.md`: Modelagem esperada, *Naming Conventions* de tabelas e diretrizes de integridade.
- `e_sql_rules.md`: Instruções sobre dialetos SQL, CTEs compulsórias e performance de consultas.
- `f_testing_rules.md`: Estrutura base para suítes `pytest`.
- `g_documentation_rules.md`: Templates de Readmes.
- `h_project_ready_rules.md`: Limites severos de Gates (o que constitui estar Pronto).

## Padrões e Decisões (`c_patterns/`, `e_decisions/`)
- O `c_brain` gerencia de forma centralizada os registros de padrões de código e decisões arquiteturais.
- `e_decisions/`: Armazena decisões tomadas dentro do log de memória do projeto para que refatorações subsequentes compreendam por que uma determinada biblioteca ou dialeto foi escolhido.

## Learning Engine (Fora do Golden Path)
O módulo `h_learning_engine.py` é um componente experimental e encontra-se **estritamente fora do Golden Path** oficial. A esteira principal de geração do AAF não executa nem depende do Learning Engine para alcançar o estado final `PROJECT READY`.

## Relação com o Graph
Embora haja integração baseada em grafos do Obsidian (`.obsidian/`), o Graph **não é o SSOT** (Single Source of Truth) e não contém regras de lógica da plataforma. O Graph atua como visualização de rede, mas a verdade emana puramente da estrutura em disco legível do Brain.
