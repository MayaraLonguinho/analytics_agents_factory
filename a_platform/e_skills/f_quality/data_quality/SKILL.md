---
name: data-quality
description: Asserções de qualidade de dados de saída, completude, frescor e relatórios de evidências.
---

# Data Quality Skill

## Purpose
Validar a qualidade e integridade dos resultados finais gerados pelo pipeline (ausência de nulos indevidos, validação de ranges, métricas de conformidade e geração de evidência de qualidade).

## When to use
- Na etapa de validação da saída dos pipelines de dados e analytics.

## When not to use
- Para testes unitários de código ou funções puras.

## Inputs
- `task_description` (string, optional): Regras e tolerâncias de qualidade.

## Outputs
- `data_quality.py` (string): Código executável de checagens de qualidade de dados.

## Capabilities
- data-quality
- completeness-checks
- freshness-checks
- sanity-checks

## Constraints
- Proibido simular aprovação falsa; checagens devem falhar caso evidências violem as regras.
