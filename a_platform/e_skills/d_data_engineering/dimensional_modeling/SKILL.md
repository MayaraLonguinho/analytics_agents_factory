---
name: dimensional-modeling
description: Modelagem dimensional de dados (Star Schema, tabelas fato e dimensões).
---

# Dimensional Modeling Skill

## Purpose
Projetar schemas dimensionais (Star Schema ou Snowflake Schema), definindo tabelas fato, tabelas dimensão, chaves substitutas (surrogate keys) e grãos de análise para data warehouses ou data marts.

## When to use
- Quando o projeto demandar estruturação analítica formal para BI ou data warehouse.

## When not to use
- Para modelagem transacional OLTP normalizada (3NF).

## Inputs
- `task_description` (string, optional): Entidades e métricas de negócio.

## Outputs
- `dimensional_model.sql` (string): DDL com tabelas fato e dimensão.

## Capabilities
- dimensional-modeling
- star-schema
- fact-tables
- dimension-tables
- surrogate-keys

## Constraints
- Declarar explicitamente a chave e o grão de cada tabela fato.
