---
name: pipeline-observability
description: Instrumentação de observabilidade, logging estruturado, contadores e métricas de execução.
---

# Pipeline Observability Skill

## Purpose
Instrumentar scripts e pipelines de dados com logging estruturado, cronômetros de etapas, contadores de registros e rastreamento de linhagem de execução.

## When to use
- Para enriquecer pipelines com monitoramento e diagnóstico de execução.

## When not to use
- Para transformações ou consultas SQL isoladas.

## Inputs
- `task_description` (string, optional): Requisitos de logging e observabilidade.

## Outputs
- `observability.py` (string): Código de instrumentação e logging.

## Capabilities
- pipeline-observability
- structured-logging
- execution-metrics
- lineage-tracking

## Constraints
- Formato de logs limpo compatível com terminal e arquivos de log.
