---
name: analytics-engineering
description: Modelagem e transformação modular (staging, intermediate, marts) no ecossistema analítico.
---

# Analytics Engineering Skill

## Purpose
Estruturar camadas modulares de transformação de dados (stg_*, int_*, fct_*, dim_*), organizando dependências entre modelos e definindo regras canônicas de consumo analítico.

## When to use
- Quando o projeto exigir organização em camadas analíticas modulares (seja em SQL nativo ou dbt se planejado).

## When not to use
- Para pipelines de ingestão de arquivos brutos.

## Inputs
- `task_description` (string, optional): Camadas e modelos analíticos desejados.

## Outputs
- `analytics_models.sql` (string): Código SQL dos modelos analíticos modulares.

## Capabilities
- analytics-engineering
- modular-models
- staging-models
- marts-models

## Constraints
- dbt é suportado como possibilidade quando previsto no plano, não dependência obrigatória.
