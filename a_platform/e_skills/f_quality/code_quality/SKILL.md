---
name: code-quality
description: Testes automatizados essenciais via Pytest, cobertura de regras críticas e validação de código.
---

# Code Quality Skill

## Purpose
Gerar suítes de testes automatizados com Pytest (`test_pipeline.py`) cobrindo as funções essenciais de ETL, transformações de limpeza, inserção no banco e geração de arquivos analíticos.

## When to use
- Na camada de testes (`TestingLayer`) do projeto gerado para validar a implementação.

## When not to use
- Para testes manuais ou checagens ad-hoc não executáveis.

## Inputs
- `task_description` (string, optional): Casos de teste e funções a cobrir.

## Outputs
- `test_pipeline.py` (string): Código de teste executável por pytest.

## Capabilities
- code-quality
- unit-testing
- pytest-generation
- pipeline-testing

## Constraints
- Testes reais e objetivos, sem mocks excessivos que escondam erros de execução física.
