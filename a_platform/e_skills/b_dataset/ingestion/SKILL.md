---
name: data-ingestion
description: Gera lógica e scripts para ingestão robusta de fontes de dados tabulares.
---

# Data Ingestion Skill

## Purpose
Gerar código de ingestão e carregamento de dados a partir de fontes locais ou remotas (CSV, JSON, Parquet, bancos de dados), com suporte a validação de formato e tratamento de erros de leitura.

## When to use
- Ao construir a camada inicial de pipelines de dados.
- Quando for necessário carregar fontes brutas em dataframes ou tabelas de staging.

## When not to use
- Para transformações analíticas avançadas.
- Para profiling estatístico.

## Inputs
- `dataset_path` (string, optional): Caminho do arquivo a ser ingerido.
- `source_type` (string, optional): Tipo da fonte (csv, parquet, json, database). Default: csv.

## Outputs
- `ingestion.py` (string): Código Python com a lógica de ingestão robusta.

## Capabilities
- data-ingestion
- csv-reading
- source-loading
- error-handling

## Constraints
- Deve incluir tratamento para arquivos inexistentes e encodings inconsistentes.

## Execution guidance
- Executado por DataAgent durante a fase de ingestão de dados.
