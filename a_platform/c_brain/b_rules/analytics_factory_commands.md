## PROTOCOLO OBRIGATÓRIO DE OPERAÇÃO DO ANALYTICS AI FACTORY (AAF)

1. COMANDOS DE ATIVAÇÃO:
   - `aaf start`: Inicia nova solicitação de projeto através do AAF.
   - `aaf continue <project_id>`: Retoma sessão existente com as respostas do Discovery.
   - `aaf status <project_id>`: Consulta o estado atual da esteira.

2. REGRA DE DELEGAÇÃO EXCLUSIVA:
   - O Agent da IDE NUNCA deve gerar arquivos de código, scripts ETL, APIs ou interfaces frontend diretamente no workspace.
   - O Agent da IDE DEVE instanciar e executar o AAF através da interface oficial `IDEAdapter` (executando o runner Python correspondente a `IDEAdapter.create_project()` ou `IDEAdapter.continue_project()`).

3. FLUXO INTERATIVO:
   - Quando o AAF retornar status `NEEDS_INPUT`, o Agent da IDE repassa as perguntas de refinamento ao usuário no chat.
   - Ao receber a resposta, o Agent da IDE envia as respostas via `IDEAdapter.continue_project(project_id, answers)`.

4. PROIBIÇÃO DE FALLBACK MANUAL:
   - Se o AAF falhar em qualquer etapa (Discovery, Planning, Materialization, Execution, Validation, Quality, Certification), o Agent da IDE DEVE informar o erro e registrar `PROJECT READY = NO`.
   - É EXPRESSAMENTE PROIBIDO ao Agent da IDE criar o projeto manualmente fora do AAF para contornar a falha.
