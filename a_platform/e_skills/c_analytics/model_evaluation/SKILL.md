---
name: model-evaluation
description: Avaliação de performance de modelos de ML com métricas e matrizes de confusão.
---

# Model Evaluation Skill

## Purpose
Computar métricas formais de avaliação de modelos (MAE, RMSE, R2, ROC-AUC, Precisão, Recall, F1-Score, matriz de confusão) em conjuntos de teste isolados.

## When to use
- Após o treinamento de modelos preditivos para certificar a qualidade do modelo.

## When not to use
- Em análises descritivas ou pipelines sem aprendizado supervisionado.

## Inputs
- `task_description` (string, optional): Métricas específicas requeridas.

## Outputs
- `evaluate.py` (string): Código de avaliação do modelo.

## Capabilities
- model-evaluation
- metrics-computation
- classification-report
- residual-analysis

## Constraints
- Avaliação realizada estritamente sobre o conjunto de teste desacoplado.
