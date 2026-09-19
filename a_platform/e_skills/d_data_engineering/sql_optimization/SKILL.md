---
name: sql-optimization
description: Otimização de consultas SQL, criação de índices e melhoria de planos de execução.
---

# SQL Optimization Skill

## Purpose
Analisar e reescrever queries SQL lentas, sugerir índices adequados, evitar full table scans e aplicar padrões de alta performance compatíveis com OLTP/OLAP.

## When to use
- Quando queries existentes precisarem de refatoração para ganho de performance.

## When not to use
- Para criação de consultas triviais simples.

## Inputs
- `task_description` (string, optional): Query original e problema de performance relatado.

## Outputs
- `optimized_queries.sql` (string): Código SQL otimizado e índices recomendados.

## Capabilities
- sql-optimization
- index-design
- query-performance
- execution-plans

## Constraints
- Garantir que a query otimizada produza o mesmo resultado semântico que a original.
