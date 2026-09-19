---
name: exploratory-data-analysis
description: Executa análise exploratória de dados estruturados gerando relatórios descritivos.
---

# Exploratory Data Analysis (EDA) Skill

## Purpose
Gerar código e relatórios de análise exploratória de dados (EDA), analisando distribuições, correlações, cardinalidade e padrões em variáveis numéricas e categóricas.

## When to use
- Quando o usuário ou o plano solicitar explicitamente exploração ou análise detalhada de dados.
- Para obter insights estatísticos descritivos antes de modelagem.

## When not to use
- Para pipelines de ETL operacionais simples que apenas movem dados.

## Inputs
- `task_description` (string, optional): Requisitos específicos da exploração.
- `dataset_path` (string, optional): Caminho do dataset para exploração.

## Outputs
- `eda.py` (string): Código executável de análise exploratória.

## Capabilities
- eda
- descriptive-statistics
- correlation-analysis
- distribution-analysis
- outlier-analysis

## Constraints
- Análise baseada estritamente em evidências observadas nos dados, sem conclusões inventadas.
