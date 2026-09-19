---
name: feature-selection
description: Seleção de variáveis preditivas relevantes e redução de dimensionalidade.
---

# Feature Selection Skill

## Purpose
Identificar e selecionar as variáveis de maior poder preditivo através de testes estatísticos, importância baseada em modelos (tree-based) ou eliminação recursiva.

## When to use
- Em projetos com datasets de alta dimensionalidade destinados a modelos de ML.

## When not to use
- Para projetos descritivos ou ETL sem componente preditivo.

## Inputs
- `task_description` (string, optional): Requisitos da seleção de atributos.

## Outputs
- `feature_selection.py` (string): Código de seleção de atributos.

## Capabilities
- feature-selection
- feature-importance
- dimensionality-reduction

## Constraints
- Manter interpretabilidade e documentar critérios de corte.
