---
name: model-training
description: Treinamento de modelos preditivos ou classificadores estruturados.
---

# Model Training Skill

## Purpose
Gerar código para divisão treino/teste, instanciação, ajuste de hiperparâmetros e treinamento de modelos de machine learning (regressão, classificação ou clustering).

## When to use
- Quando o escopo do projeto incluir entrega de modelo preditivo.

## When not to use
- Para projetos padrão de analytics descritivo ou engenharia de dados.

## Inputs
- `task_description` (string, optional): Descrição do problema de modelagem.

## Outputs
- `train.py` (string): Código de treino do modelo.

## Capabilities
- model-training
- cross-validation
- hyperparameter-tuning

## Constraints
- Salvar artefato do modelo treinado (ex: .joblib ou .pkl) quando indicado.
