---
name: dataset-profiling
description: Analisa estrutura, schema, tipos e qualidade inicial de um dataset físico.
---

# Dataset Profiling Skill

## Purpose
Inspecionar deterministicamente datasets físicos (CSV, JSON, etc.) para extrair contagem de linhas e colunas, tipos inferidos, valores nulos e duplicatas sem uso de suposições ou LLM.

## When to use
- Quando um dataset de entrada for fornecido no início do pipeline.
- Antes da tomada de decisões arquiteturais que dependem da estrutura física dos dados.

## When not to use
- Quando não há arquivo físico disponível.
- Para gerar código ou scripts ETL.

## Inputs
- `dataset_path` (string, required): Caminho para o arquivo de dados.

## Outputs
- `profile` (dict): Estatísticas detalhadas incluindo contagem de linhas, colunas, tipos e duplicatas.

## Capabilities
- profiling
- schema-analysis
- duplicate-detection
- missing-values

## Constraints
- Execução determinística local via Pandas sem chamadas a LLM.
- Não altera o arquivo de entrada.

## Execution guidance
- Utilizar `DatasetProfilingSkill.execute(context)` passando `dataset_path`.
