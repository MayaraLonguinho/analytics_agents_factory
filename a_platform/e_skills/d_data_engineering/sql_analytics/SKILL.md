---
name: sql-analytics
description: Geração de consultas analíticas SQL otimizadas com CTEs, window functions e agregações.
---

# SQL Analytics Skill

## Purpose
Gerar consultas SQL analíticas limpas e idiomáticas (SELECT, JOIN, GROUP BY, CTEs, Window Functions), compatíveis com a tecnologia de banco definida no projeto (SQLite, PostgreSQL, DuckDB).

## When to use
- Ao gerar queries de relatórios, agregação de métricas ou visões analíticas.

## When not to use
- Para criação de DDL pura de infraestrutura de banco.

## Inputs
- `database_technology` (string, optional): Tecnologia do banco de dados (ex: SQLite). Default: SQLite.
- `schema_definition` (string, optional): Schema das tabelas envolvidas.
- `task_description` (string, optional): Perguntas de negócio e métricas a calcular.

## Outputs
- `analytics.sql` (string): Código SQL analítico.

## Capabilities
- sql
- joins
- aggregations
- cte
- window-functions

## Constraints
- Respeitar estritamente o dialeto SQL da tecnologia de banco selecionada.
