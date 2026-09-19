---
name: architecture-documentation
description: Documentação arquitetural com limites do sistema, componentes, dependências e diagramas C4/Mermaid.
---

# Architecture Documentation Skill

## Purpose
Documentar as decisões arquiteturais, limites de sistema (system context), diagrama de componentes e fluxos de dados utilizando notação C4 ou Mermaid quando aplicável.

## When to use
- Quando a solução demandar documentação formal de arquitetura e decisões (ADRs).

## When not to use
- Em projetos mínimos de script único onde o README basilar for suficiente.

## Inputs
- `task_description` (string, optional): Detalhes da arquitetura.

## Outputs
- `ARCHITECTURE.md` (string): Documento formal de arquitetura em Markdown.

## Capabilities
- architecture-documentation
- c4-model
- component-diagrams
- architecture-decisions

## Constraints
- Diagramas devem usar sintaxe Mermaid válida sem tags HTML nos rótulos.
