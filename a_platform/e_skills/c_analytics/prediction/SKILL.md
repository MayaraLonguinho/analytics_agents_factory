---
name: prediction
description: Inferência e geração de previsões em novos dados utilizando modelos treinados.
---

# Prediction Skill

## Purpose
Gerar código de inferência em lote (batch) ou unitária a partir de modelos persistidos, validando o schema de entrada e produzindo colunas com os scores e previsões.

## When to use
- Quando o pipeline final exigir escoragem ou predição sobre novos registros.

## When not to use
- Em análises puramente descritivas ou ETL sem inferência preditiva.

## Inputs
- `task_description` (string, optional): Requisitos da inferência.

## Outputs
- `predict.py` (string): Código de inferência com o modelo.

## Capabilities
- prediction
- model-inference
- batch-scoring

## Constraints
- Validar compatibilidade de tipos com as features de treino.
