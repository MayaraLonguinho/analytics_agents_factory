---
name: technical-documentation
description: Geração de documentação técnica, especificações de componentes e guias operacionais.
---

# Technical Documentation Skill

## Purpose
Gerar documentação técnica detalhada cobrindo fluxos de dados, dicionários de dados, contratos de interfaces e guias operacionais do sistema.

## When to use
- Na camada de documentação do projeto gerado pela fábrica.

## When not to use
- Para código executável ou testes unitários.

## Inputs
- `task_description` (string, optional): Requisitos da documentação.

## Outputs
- `TECHNICAL_DOCS.md` (string): Documentação técnica completa em Markdown.

## Capabilities
- technical-documentation
- runbooks
- system-specs
- data-dictionary

## Constraints
- Baseada estritamente na arquitetura e artefatos reais gerados pelo pipeline.
