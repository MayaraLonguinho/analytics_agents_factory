# Comandos do Analytics AI Factory

O agente da IDE (Cursor, Devin, Copilot, etc.) deve interagir com o Analytics AI Factory EXCLUSIVAMENTE através da sua interface oficial via `main.py`.

## Protocolo de Ativação Inegociável

QUANDO O USUÁRIO DIGITAR QUALQUER UM DESTES COMANDOS:
- `aaf start`
- `aaf run`
- `aaf create`
- `aaf continue <project_id>`
- `aaf status <project_id>`

REGRA ABSOLUTA DE EXECUÇÃO:
1. O Agente da IDE NÃO DEVE gerar arquivos de código, scripts ETL, APIs ou componentes frontend manualmente. É EXPRESSAMENTE PROIBIDO!
2. O Agente da IDE DEVE acionar o Analytics AI Factory através da execução do arquivo `main.py` do repositório. Exemplo: `python main.py start "seu prompt"`
3. Se o AAF retornar status `NEEDS_INPUT` ou `PAUSED`, o Agente da IDE repassa as perguntas ao usuário no chat e, após a resposta, chama `python main.py continue <project_id> "resposta"`.
4. Se o AAF falhar e retornar `FAILED`, o Agente da IDE reporta a falha. É EXPRESSAMENTE PROIBIDO fazer fallback para criação manual de código fora do AAF.