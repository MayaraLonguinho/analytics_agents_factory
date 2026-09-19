---
name: discover-intent
description: Extração estruturada de intenção e requisitos a partir de solicitações em linguagem natural.
---

# Intent Discovery Skill

## Purpose
Extrair intenção, domínio técnico, entidades e requisitos funcionais a partir de solicitações em linguagem natural enviadas pelo usuário.

## When to use
- Na fase inicial de Discovery.

## When not to use
- Para execução ou materialização de código.

## Inputs
- `request_text` (string, required): Texto da solicitação do usuário.

## Outputs
- `intent` (dict): Intenção estruturada extraída.

## Capabilities
- intent-discovery
- requirements-parsing
- domain-detection

## Constraints
- Operar conforme os limites e regras do DiscoveryAgent.
