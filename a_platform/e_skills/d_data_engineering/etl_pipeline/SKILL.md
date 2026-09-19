---
name: etl-pipeline
description: Pipeline de ETL/ELT determinístico, modular e tipado em Python (Pandas/Polars/DuckDB).
---

# ETL Pipeline Skill

## Purpose
Gerar o script principal do pipeline de dados com fluxo completo: leitura da fonte, limpeza/sanitização, transformações determinísticas, carga em banco relacional local (ex: SQLite) e relatórios.

## When to use
- Como componente central em qualquer projeto de Data Engineering gerado pela fábrica.

## When not to use
- Para projetos puramente de análise SQL ad-hoc sem movimentação de dados.

## Inputs
- `data_processing_tool` (string, optional): Ferramenta utilizada (ex: Pandas). Default: Pandas.
- `task_description` (string, optional): Detalhes dos requisitos do pipeline.

## Outputs
- `pipeline.py` (string): Código executável completo do pipeline de dados.

## Capabilities
- etl-pipeline
- data-extraction
- data-loading
- pipeline-orchestration

## Constraints
- Sem preenchimentos arbitrários de dados; código deve ser executável diretamente por `python pipeline.py`.
