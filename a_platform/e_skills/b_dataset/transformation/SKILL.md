---
name: data-transformation
description: Aplica transformações estruturadas, regras de negócio e tipagem a dados tabulares.
---

# Data Transformation Skill

## Purpose
Aplicar transformações estruturadas em datasets, tais como derivação de colunas, normalização, filtros de negócio e remodelagem tabular.

## When to use
- Durante o pipeline de ETL após a etapa de limpeza.
- Para preparar dados para persistência relacional ou modelos analíticos.

## When not to use
- Para profiling ou ingestão inicial de arquivos.

## Inputs
- `task_description` (string, optional): Descrição das regras de transformação.
- `schema_definition` (string, optional): Esquema alvo esperado.

## Outputs
- `transformation.py` (string): Código Python com a lógica de transformação.

## Capabilities
- data-transformation
- type-casting
- business-rules
- schema-alignment

## Constraints
- Deve preservar consistência e tipos esperados no destino.
