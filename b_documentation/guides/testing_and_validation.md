# Roteiro de Testes e Homologação Manual

## Execução da Suíte Automatizada
Para rodar a suíte completa de testes automatizados, certifique-se de que o ambiente virtual está ativado e execute:
```bash
pytest -v
```
A aprovação sem falhas garante que os componentes core e a árvore canônica estão em pleno funcionamento.

## Roteiro de Homologação Manual Passo a Passo

1. **Preparação de Dataset:** Coloque seu arquivo de teste (ex: `vendas.csv`) em `d_input/a_datasets/a_raw/vendas.csv`.
2. **Disparo da Solicitação:** Inicie via IDE Chat ou CLI pedindo a criação de um pipeline.
3. **Discovery:** Valide se o portão de Discovery atinge o status `COMPLETE`.
4. **Profiling e Planning:** Verifique se a análise de dados e a criação do DAG do Planner retornam `COMPLETE`.
5. **Materialization:** Acesse a pasta `e_generated_projects/<domain>/<project_id>/` e verifique se o código-fonte foi escrito com status `SUCCESS`.
6. **Execution Runtime:** Valide a execução física com `SUCCESS` (criação de venv filho, dependências e processamento).
7. **Validation Gate:** O projeto gerado deve rodar o `pytest` interno, retornando `PASS`.
8. **Repair Loop:** Caso o teste gerado falhe inicialmente, verifique os logs para confirmar o acionamento do Repair Loop e correção.
9. **Quality e Certification:** Confirme que o linter e as métricas reportam `PASS` e o `CERTIFICATION.md` é gerado.
10. **Readiness Gate:** Verifique a regra estrita no final dos logs:

```text
Discovery       = COMPLETE
Planning        = COMPLETE
Materialization = SUCCESS
Execution       = SUCCESS
Validation      = PASS
Quality         = PASS
Certification   = PASS
-----------------------------
PROJECT READY   = YES
```

## Limpeza de Artefatos
Após os testes, limpe os projetos gerados e o estado da plataforma executando:
```bash
# Limpeza de projetos (mantendo .gitkeep)
find e_generated_projects -mindepth 1 ! -name ".gitkeep" -exec rm -rf {} +

# Limpeza de estados de projetos (mantendo .gitkeep)
find .aaf_state -mindepth 1 ! -name ".gitkeep" -exec rm -rf {} +
```
*Em sistemas sem o comando find (como Windows CMD default), a remoção pode ser feita deletando o conteúdo das pastas manualmente, preservando o arquivo .gitkeep.*
