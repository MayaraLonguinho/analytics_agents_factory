---
name: dataset-validation
description: Validação estrutural e integridade do dataset de entrada antes do processamento.
---

# Dataset Validation Skill

## Purpose
Validar se o dataset de entrada está conforme os contratos esperados: presença das colunas obrigatórias, tipos compatíveis, ausência de nulos em chaves primárias e conformidade estrutural.

## When to use
- Antes de iniciar etapas destrutivas ou transformações no dataset.
- Para assegurar que o input recebido respeita o contrato do pipeline.

## When not to use
- Para validar artefatos ou testes de código gerado (usar quality skills).

## Inputs
- `schema_definition` (string, optional): Esquema esperado das colunas e tipos.
- `dataset_path` (string, optional): Caminho do dataset a validar.

## Outputs
- `dataset_validator.py` (string): Código de validação pré-execução.

## Capabilities
- dataset-validation
- schema-verification
- input-contract-checks
- integrity-verification

## Constraints
- Focado na validação do input, não na validação de saída de testes.
