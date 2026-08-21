# Diretório de Regras do Devin

## Objetivo

Este diretório contém regras específicas da integração do Devin com o Analytics AI Factory.

## Responsabilidade

As regras deste diretório determinam como o Devin deve:

- reconhecer comandos;
- encaminhar solicitações;
- utilizar o AAF;
- respeitar a separação entre integração e núcleo;
- lidar com projetos gerados.

As regras canônicas do Analytics AI Factory pertencem ao núcleo do AAF.

## Regra Principal

O Devin não deve duplicar regras de negócio ou regras arquiteturais do Analytics AI Factory.

Quando uma regra pertence ao funcionamento do produto, ela deve ser mantida no núcleo do AAF.

## Regras Disponíveis

- [Comandos do Analytics AI Factory](analytics_factory_commands.md) — regras para reconhecimento e encaminhamento dos comandos.

## Domínios da Primeira Versão

O adaptador deve reconhecer prioritariamente:

- Analytics;
- Data Engineering.

Outros domínios não devem ser tratados como implementações ativas nesta primeira versão.