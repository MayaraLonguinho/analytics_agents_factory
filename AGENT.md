# IDE Agent Integration Rules

Este arquivo define como você (IDE Agent / AI Assistant) deve interagir com a Analytics Agents Factory (AAF).

## Porta de Entrada (Entry Point)
A única porta de entrada autorizada para criar e orquestrar projetos com a fábrica é o comando:
`aaf start`

- **NÃO** crie projetos de dados manualmente através da sua rotina padrão (IDE).
- **NÃO** escreva scripts ETL, pipelines, ou rotinas de dados fora da AAF.
- Quando o usuário solicitar a criação de um pipeline, projeto analítico, dashboard ou estrutura de engenharia de dados, você deve orientá-lo a rodar `./aaf start` ou você mesmo deve executar esse comando para ele no terminal integrado.

## Tratamento de Falhas e Interrupções
O comando `aaf start` invocará o `IDEAdapter` e iniciará uma sessão.
Caso a fábrica pare durante o Discovery aguardando input (status `NEEDS_INPUT`), interaja com o prompt de terminal, ou peça para o usuário interagir com o prompt fornecendo o contexto necessário.

### PROJETO READY = NO
Se por qualquer motivo o processo falhar e a AAF retornar `PROJECT READY = NO` (Status: FAILED):
- **NÃO** tente corrigir o código, a compilação ou o pipeline manualmente. 
- O Master Orchestrator da AAF possui as próprias rotinas de validação e *repair loop*.
- Se a AAF falhou definitivamente, o projeto não está pronto. Você deve apenas informar o erro que foi retornado pela fábrica.

## Consulta de Status
Você pode utilizar `./aaf status <project_id>` ou `./aaf result <project_id>` para reportar o andamento ou consultar os artefatos de saída gerados sem ter que navegar nas subpastas manualmente.
