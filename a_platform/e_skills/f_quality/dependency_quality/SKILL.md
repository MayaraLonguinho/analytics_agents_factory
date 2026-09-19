---
name: dependency-quality
description: Geração, fixação de versões e auditoria de dependências mínimas em requirements.txt.
---

# Dependency Quality Skill

## Purpose
Gerar o arquivo `requirements.txt` estritamente necessário para o projeto, com pinagem de versões compatíveis, sem pacotes supérfluos ou vulnerabilidades conhecidas.

## When to use
- Na finalização do projeto gerado para garantir reprodutibilidade da instalação via pip.

## When not to use
- Para instalar pacotes em tempo de execução.

## Inputs
- `task_description` (string, optional): Bibliotecas requeridas no projeto.

## Outputs
- `requirements.txt` (string): Lista de dependências pinadas.

## Capabilities
- dependency-quality
- package-pinning
- requirements-generation
- vulnerability-audit

## Constraints
- Conter apenas as dependências declaradas e de fato utilizadas no código gerado.
