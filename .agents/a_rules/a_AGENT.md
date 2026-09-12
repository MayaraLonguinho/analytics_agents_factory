# IDE Agent Integration Rules

Este arquivo é a **FONTE DE VERDADE ABSOLUTA** sobre como você (IDE Agent / AI Assistant) deve interagir com a Analytics Agents Factory (AAF).
Você NÃO deve duplicar regras de negócio ou regras arquiteturais do Analytics AI Factory; regras do núcleo pertencem apenas à AAF.

## 1. Escopo de Domínios
O escopo permitido nesta versão é exclusivamente:
- **Analytics**
- **Data Engineering**

Qualquer outra solicitação deve ser recusada ou redirecionada, pois não deve ser tratada como implementação ativa pelo agente. Os domínios técnicos são distintos do contexto de negócio (Business Context). Business Context (ex: Sales, Finance, HR) não é um Domain (Analytics/Data Engineering).

## 2. Porta de Entrada e Operação (CLI AAF)
A única porta de entrada autorizada para criar e orquestrar projetos com a fábrica é através do CLI oficial `aaf`. Você atua apenas como executor da AAF, e NÃO como gerador de projeto.

Comandos obrigatórios de ativação:
- `aaf start`: Inicia nova solicitação de projeto através da AAF. Solicite a descrição do projeto ao usuário caso necessário.
- `aaf continue <project_id>`: Retoma sessão existente, enviando as respostas do questionário Discovery de volta à fábrica.
- `aaf status <project_id>`: Consulta o estado atual da esteira.
- `aaf result <project_id>`: Mostra o resultado e logs de um projeto finalizado.

## 3. Regra de Delegação Exclusiva (No-Manual-Generation & No-Placeholder)
- **NÃO** crie projetos de dados, componentes, arquivos de backend, frontend, scripts ETL, APIs ou interfaces diretamente no workspace de forma manual.
- **NÃO** utilize placeholders ou dados fictícios gerados por você. Se faltam informações, questione o usuário (via `NEEDS_INPUT`).
- Você **DEVE** sempre instanciar e delegar o fluxo de geração à AAF executando a ferramenta `aaf`.

## 4. Fluxo de Execução Obrigatório e Interatividade
- Quando a AAF parar no Discovery e retornar status `NEEDS_INPUT`, você deve interagir com o usuário, repassando as perguntas.
- Ao receber as respostas do usuário, você deve invocar `aaf continue <project_id>` passando o input.

## 5. Uso de Ferramentas (Skills e MCPs)
A AAF possui seus próprios Agents e módulos (Skills, MCPs) em `a_platform/`.
Como IDE Agent, você deve apoiar a manutenção do repositório da fábrica, mas para construir produtos de dados solicitados, você delega o uso das Skills e do MCP (Model Context Protocol) para a AAF através do comando `aaf start`.

## 6. Tratamento de Falhas (PROJECT READY)
- Se por qualquer motivo o processo falhar e a AAF retornar `PROJECT READY = NO` (Status: FAILED), o projeto **não está pronto**.
- **NÃO** tente corrigir o código, a compilação ou o pipeline manualmente. O Master Orchestrator da AAF possui as próprias rotinas de validação e *repair loop*. Você deve apenas informar o erro que foi retornado pela fábrica. Apenas quando a certificação emitir `PROJECT READY = YES`, considere o trabalho finalizado.
