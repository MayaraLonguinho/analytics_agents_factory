# Context do Brain

## Finalidade

O Context Manager é responsável por organizar as informações utilizadas pelo Brain durante uma execução.

## Responsabilidades

- manter contexto da sessão;
- incorporar informações do usuário;
- incorporar informações recuperadas pelo RAG;
- atualizar contexto;
- fornecer contexto aos componentes superiores.

## Separação

Context não é:

- Knowledge;
- Memory;
- RAG;
- Agent;
- Planning.

Ele atua como camada de composição entre essas informações.

## Configuração

A configuração atual é fornecida por `BrainConfig`.

## Regra

O Context Manager não deve armazenar permanentemente conhecimento do AAF.

Conhecimento permanente pertence ao Knowledge.

Estado de execução pertence à Memory.