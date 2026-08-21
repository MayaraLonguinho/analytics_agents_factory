# Diretório de Workflows do Devin

## Objetivo

Este diretório contém os workflows específicos da integração do Devin com o Analytics AI Factory.

## Responsabilidade

Os workflows determinam como o Devin encaminha operações para o AAF.

Eles não devem implementar diretamente a lógica de:

- Discovery;
- Dataset Profiling;
- Brain;
- Planning;
- Factory;
- Materialization;
- Runtime;
- Validation;
- Quality;
- Certification.

## Workflow Disponível

- [Workflow do Analytics AI Factory](analytics_factory_workflow.md) — fluxo de integração entre Devin e AAF.

## Núcleo

O fluxo real do Analytics AI Factory pertence ao núcleo do projeto.

O Devin apenas inicia ou encaminha as operações através das interfaces oficiais.