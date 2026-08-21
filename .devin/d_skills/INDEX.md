# Diretório de Skills do Devin

## Objetivo

Este diretório contém skills específicas da integração do Devin com o Analytics AI Factory.

## Responsabilidade

As skills deste diretório funcionam como adaptadores entre o Devin e as capacidades do AAF.

As skills canônicas do Analytics AI Factory pertencem ao núcleo:

`e_skills/`

Este diretório não deve conter uma segunda implementação das skills canônicas.

## Skill Disponível

- [Analytics Factory Skill](analytics_factory_skill.py) — integração para execução de comandos do Analytics AI Factory.

## Relação com o Núcleo

A skill do Devin utiliza as interfaces disponibilizadas pelo AAF.

O Devin não deve implementar diretamente:

- profiling;
- ETL;
- analytics;
- database;
- visualization;
- ML;
- validation;
- certification.

Essas capacidades pertencem ao núcleo do Analytics AI Factory.

## Regra de Independência

As skills do núcleo devem continuar funcionando sem depender do Devin.