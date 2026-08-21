# Diretório de Contexto do Devin

## Objetivo

Este diretório contém a configuração de integração de contexto entre o Devin e o Analytics AI Factory.

## Responsabilidade

O contexto canônico do Analytics AI Factory pertence ao núcleo do AAF.

A implementação principal ficará em:

`c_brain/d_context/`

Este diretório não deve armazenar uma segunda implementação do contexto do AAF.

## Contexto Utilizado

O Devin pode fornecer informações contextuais relacionadas à interação atual, incluindo:

- solicitação do usuário;
- comando recebido;
- sessão atual;
- informações necessárias para encaminhamento ao AAF.

## Relação com o Núcleo

O fluxo de integração é:

Devin

↓

Contexto da interação

↓

Interface do Analytics AI Factory

↓

`c_brain/d_context/`

## Independência

O contexto canônico do AAF não deve depender do Devin.

O Analytics AI Factory deve continuar funcionando independentemente do ambiente de integração utilizado.