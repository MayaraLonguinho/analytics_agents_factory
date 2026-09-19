---
name: metrics-analysis
description: Cálculo e agregação de métricas de negócio, KPIs, faturamentos e volumes.
---

# Metrics Analysis Skill

## Purpose
Gerar código de cálculo de métricas analíticas e de negócio, totalizadores, taxas de conversão, ticket médio, agregações multidimensionais e resumos gerenciais.

## When to use
- Quando o projeto exigir entrega de resumos de KPIs ou consolidações analíticas.

## When not to use
- Para transformações básicas de ETL sem agregação analítica.

## Inputs
- `task_description` (string, optional): Descrição das métricas e dimensões esperadas.

## Outputs
- `metrics.py` (string): Código executável para cálculo das métricas.

## Capabilities
- metrics-analysis
- kpi-calculation
- aggregations
- business-metrics
- dimensional-breakdown

## Constraints
- Fórmulas de métricas devem respeitar estritamente as definições solicitadas.
