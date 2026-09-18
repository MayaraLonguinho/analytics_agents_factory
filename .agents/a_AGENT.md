# Regras do Agente da IDE: Analytics Agents Factory (AAF)

## 1. Identidade e Propósito
- Tratar este sistema como a Analytics Agents Factory (AAF).
- Usar a AAF para gerar projetos especializados em Analytics + ETL/ELT.
- Manter o projeto agnóstico a qualquer domínio de negócio específico.
- Utilizar somente os domínios e capacidades suportados pela arquitetura.

## 2. Fluxo de Execução Principal
Siga esta sequência exata para a geração de projetos:
1. IDE Chat
2. IDE Adapter
3. Discovery
4. Dataset Profiling
5. Brain
6. Architecture
7. Planner
8. Project Factory
9. Agents + Skills + MCPs + LLM Gateway
10. Artifact Materializer
11. e_generated_projects/
12. Execution Runtime
13. Validation Gate
14. Repair Loop
15. Quality Engine
16. Certification Engine
17. PROJECT READY

Respeite a restrição de sequência: `Context → Plan → Decisions → Skills → Gates`

## 3. Protocolo de Discovery
- Fazer no **máximo 5 perguntas** de descoberta no total.
- Fazer **uma pergunta por vez**.
- Só perguntar quando a resposta puder alterar arquitetura, escopo, capacidade, fonte, destino ou critério de aceite.
- Converter pequenas incertezas em **assumptions** (premissas) declaradas.
- Registrar decisões não resolvidas como `Q-NN`.

## 4. Limites Operacionais
- **Do not execute Git commands anywhere in this project.** (Não executar comandos Git em nenhum lugar deste projeto). Isto inclui comandos utilizados apenas para inspeção, como git status, git log, etc.
- Não inventar regras de negócio.
- Não gerar placeholders, mocks ou TODOs.
- Não aceitar "fake success" (falso sucesso) como implementação.
- Não marcar o projeto como `PROJECT READY` sem evidência real de que passou em todos os gates.
- Não construir manualmente um projeto se a automação da AAF falhar. Se a geração falhar, apenas reporte a falha.
- Respeitar sempre os gates de validação e qualidade.

## 5. Padrões Arquiteturais
- Manter **Modular Monolith** (Monolito Modular) como padrão arquitetural.
- Não criar microserviços no MVP.
- **Documentation (Documentação) não substitui a implementação.**
- **Graph (Grafo) não substitui o Brain.**

## 6. Agentes e Skills
- Agentes devem utilizar **Skills reais** do registry.
- Respeitar a hierarquia: `Planner → Task.skills → Agent → SkillRegistry`
- Agentes não devem escolher arbitrariamente suas próprias Skills.

## 7. Interfaces e Integrações
- Todos os LLMs devem ser acessados estritamente pelo **LLM Gateway**.
- Agentes não devem conhecer diretamente as SDKs da OpenAI/Gemini/Anthropic.
- **MCPs** devem obedecer aos seus contratos e limites definidos.
- O **Runtime** deve executar e validar o projeto realmente gerado, não um mock.

## 8. Separação Estrita de Papéis: IDE Agent vs AAF Native Agents
- **O IDE Chat é estritamente interface e transporte:** Quando a operação envolver a AAF (`aaf start`, comandos de geração), o Agente da IDE atua unicamente transportando comandos, exibindo perguntas pendentes ao usuário e repassando suas respostas à CLI/Adapter.
- **DiscoveryAgent realiza o Discovery:** O Agente da IDE NUNCA deve realizar Discovery externo por conta própria, nem iniciar fluxos paralelos de perguntas de requisitos.
- **ArchitectureAgent realiza a Arquitetura:** Todas as decisões técnicas e de stack pertencem exclusivamente ao ArchitectureAgent da plataforma.
- **PlannerAgent realiza o Planejamento:** A geração de tarefas, DAG e comandos de validação cabe exclusivamente ao PlannerAgent nativo.
- **Não substituição:** O Agente da IDE jamais substitui ou emula os agentes nativos da fábrica.
- **Não criação manual:** O Agente da IDE NUNCA deve gerar manualmente arquivos ou estruturas do projeto analítico para contornar o pipeline.
- **Não criação de scripts de contorno:** É proibido criar scripts auxiliares ou de teste ad-hoc para contornar falhas do pipeline.
- **Não modificação do AAF durante geração:** O Agente da IDE NUNCA deve alterar o código-fonte da plataforma AAF durante uma solicitação de geração de projeto para tentar reparar erros de execução do projeto gerado.
- **Transparência de falha:** Qualquer falha na esteira da AAF deve ser reportada fielmente como falha (`PROJECT READY = NO`), sem tentativas de mascaramento ou fake success.
