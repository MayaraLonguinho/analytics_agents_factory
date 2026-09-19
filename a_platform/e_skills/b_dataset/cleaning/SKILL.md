---
name: data-cleaning
description: Limpeza, sanitização, remoção de duplicatas e padronização de dados brutos.
---

# Data Cleaning Skill

## Purpose
Sanitizar e padronizar dados brutos através de remoção de caracteres espúrios, deduplicação exata ou por chaves, conversão de formatos e tratamento estrito de valores ausentes sem suposições arbitrárias.

## When to use
- Na fase inicial do pipeline de dados após a ingestão.
- Quando existem duplicatas, caracteres especiais ou formatos inconsistentes.

## When not to use
- Para transformações de negócio avançadas ou agregações analíticas.

## Inputs
- `task_description` (string, optional): Requisitos específicos de limpeza.
- `dataset_profile` (dict, optional): Perfil do dataset obtido pelo profiling.

## Outputs
- `cleaner.py` (string): Código Python com a lógica de higienização de dados.

## Capabilities
- data-cleaning
- deduplication
- missing-values-handling
- text-sanitization

## Constraints
- Proibido inventar ou preencher valores nulos sem evidência ou regra explícita.
