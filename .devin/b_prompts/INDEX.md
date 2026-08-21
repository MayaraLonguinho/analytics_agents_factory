# Reconhecimento de Comandos do Analytics AI Factory

Quando o usuário inserir um comando, verifique se ele corresponde aos padrões de comando do Analytics AI Factory.

## Comandos da Primeira Versão

Os domínios disponíveis na primeira versão são:

- `analytics`
- `data_engineering`

## Padrões de Comando

Reconhecer:

- `analytics execute`
- `data_engineering execute`
- `project create analytics`
- `project create data_engineering`
- `quality validate`
- `quality report`
- `quality summary`
- `certify validate`
- `certify certificate`
- `certify summary`

## Execução

Quando um comando válido for reconhecido:

1. encaminhe o comando para a interface oficial do Analytics AI Factory;
2. não implemente a lógica do comando dentro do adaptador Devin;
3. apresente o resultado retornado pelo AAF;
4. quando um projeto for gerado, apresente sua localização;
5. quando houver resultado de validação, apresente o status retornado pelo AAF.

## Criação de Projeto

Para uma solicitação como:

`project create analytics`

o Devin deve encaminhar a solicitação ao Analytics AI Factory.

Para:

`project create data_engineering`

o Devin deve encaminhar a solicitação ao Analytics AI Factory.

O adaptador não deve criar arquivos do projeto diretamente.

## Execução de Analytics

Para:

`analytics execute`

o Devin deve encaminhar a execução para o AAF.

## Execução de Data Engineering

Para:

`data_engineering execute`

o Devin deve encaminhar a execução para o AAF.

## Comandos de Qualidade

Os comandos:

- `quality validate`
- `quality report`
- `quality summary`

devem ser encaminhados ao componente de qualidade do AAF.

## Comandos de Certificação

Os comandos:

- `certify validate`
- `certify certificate`
- `certify summary`

devem ser encaminhados ao componente de certificação do AAF.

## Regra de Independência

O Devin não deve implementar:

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

Essas responsabilidades pertencem ao núcleo do Analytics AI Factory.