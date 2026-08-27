# Analytics AI Factory Protocol

QUANDO O USUÁRIO DIGITAR: `aaf start`, `aaf run`, `aaf continue`, `aaf status`

## REGRA ABSOLUTA DE EXECUÇÃO:
1. O Agent da IDE (Cursor, etc.) NÃO DEVE gerar arquivos de código, scripts ETL, APIs ou componentes frontend manualmente para o projeto principal.
2. O Agent da IDE DEVE acionar o Analytics AI Factory através da execução do arquivo `main.py` do repositório.
   Exemplo: `python main.py start "seu prompt"`
3. Se o AAF retornar status `NEEDS_INPUT`, o Agent da IDE repassa as perguntas ao usuário no chat e, após a resposta, chama `python main.py continue <project_id> "resposta"`.
4. Se o AAF falhar e retornar erro, o Agent da IDE reporta a falha do AAF. É EXPRESSAMENTE PROIBIDO fazer fallback para criação manual de código fora do AAF.
