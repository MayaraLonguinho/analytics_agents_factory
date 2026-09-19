---
name: readme-generation
description: Geração do README.md oficial do projeto com instruções de instalação, execução e testes.
---

# README Generation Skill

## Purpose
Gerar o README.md executivo e operacional do projeto contendo: objetivo, fonte de dados, fluxo de dados, estrutura de diretórios, dependências, comando exato de execução e resultados esperados.

## When to use
- Na finalização da materialização do projeto pela fábrica.

## When not to use
- Para documentação interna de APIs sem escopo de projeto.

## Inputs
- `task_description` (string, optional): Requisitos específicos do README.

## Outputs
- `README.md` (string): Conteúdo do README.md.

## Capabilities
- readme-generation
- execution-guide
- project-overview
- troubleshooting

## Constraints
- Deve refletir estritamente os comandos e arquivos reais gerados no projeto.
