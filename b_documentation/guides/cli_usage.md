# Guia de Uso: CLI (Interface Secundária)

A interface de linha de comando (CLI) reutiliza exatamente o mesmo núcleo do IDE Chat (`IDEAdapter` / `AAF Core`), permitindo a mesma experiência sem necessitar de uma IDE com IA integrada.

## Pré-requisito
1. Ambiente virtual ativado.
2. Arquivo `.env` configurado com as chaves de API.

## Comandos de Execução
Para iniciar um novo projeto, utilize o comando `create`:
```bash
python main.py create "Crie uma API FastAPI de gestão de usuarios com validação de dados"
```

## Exemplo de Sessão e Discovery
Durante a execução, se o Discovery Agent precisar de mais detalhes, a execução será pausada, o projeto será salvo em `.aaf_state/`, e você verá uma mensagem no terminal.

Para continuar e responder à pergunta:
```bash
python main.py continue <project_id> "O banco de dados deve ser SQLite."
```

## Localização dos Artefatos
Após as etapas de Materialization e Execution passarem com sucesso (e exibição do banner de certificação `PROJECT READY = YES`), todos os artefatos estarão disponíveis em:
`e_generated_projects/<domain>/<project_id>/`
