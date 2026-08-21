# Diretório de Agentes do Devin

## Objetivo

Este diretório representa a camada de integração entre o Devin e os agentes do Analytics AI Factory.

## Responsabilidade

Os agentes reais do Analytics AI Factory pertencem ao núcleo do AAF.

A implementação canônica dos agentes será mantida em:

`d_agents/`

Este diretório não deve conter uma segunda implementação dos agentes.

## Integração

O adaptador Devin pode encaminhar solicitações para os agentes disponíveis no núcleo do AAF.

Entre os agentes previstos para a primeira versão estão:

- Discovery;
- Architecture;
- Planner;
- Data;
- Database;
- Analytics;
- Backend;
- Frontend;
- Infrastructure;
- Testing;
- Documentation;
- Execution;
- Validation;
- Certification.

## Regra de Independência

Nenhum agente canônico deve depender de arquivos localizados em `.devin/`.

O fluxo correto é:

Devin

↓

Interface do Analytics AI Factory

↓

Agente do AAF

## Primeira Versão

Os agentes devem priorizar os domínios:

- Analytics;
- Data Engineering.

Novos domínios poderão ser adicionados futuramente sem duplicar agentes dentro de `.devin/`.