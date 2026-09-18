# Artifact

## Responsibility
Contrato Pydantic que encapsula a representação lógica de um arquivo a ser gerado (`path`, `content`, `type`, `metadata`), garantindo conformidade antes da escrita física em disco.

## Path
`a_platform/b_contracts/g_artifact.py`

## Inputs
[[Agents]]

## Outputs
Definição estruturada de arquivo (`Artifact`)

## Integrations
- [[Materializer]]

## Failure behavior
Erro de validação de schema Pydantic caso campos mandatórios estejam ausentes ou corrompidos.
