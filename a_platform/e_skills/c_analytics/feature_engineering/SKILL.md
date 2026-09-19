---
name: feature-engineering
description: Criação, codificação, escalonamento e transformação de atributos preditivos.
---

# Feature Engineering Skill

## Purpose
Gerar código de engenharia de features: encoding de variáveis categóricas, escalonamento/normalização, extração de features temporais, binning e interações.

## When to use
- Quando o projeto demandar modelagem preditiva ou machine learning.

## When not to use
- Para pipelines padrão de ETL ou relatórios descritivos.

## Inputs
- `task_description` (string, optional): Descrição das transformações de features.

## Outputs
- `feature_engineering.py` (string): Código de transformação de features.

## Capabilities
- feature-engineering
- encoding
- scaling
- datetime-features

## Constraints
- Evitar data leakage dividindo transformações após train/test split.
