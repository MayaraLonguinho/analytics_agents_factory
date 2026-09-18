# Materializer

## Responsibility
Manipulador físico de arquivos. Converte a coleção lógica de artefatos em arquivos concretos no disco, operando sob sandbox estrito dentro de `e_generated_projects/<project_id>`.

## Path
`a_platform/i_materializer/a_materializer.py`

## Inputs
[[Artifact]], [[Orchestrator]]

## Outputs
Arquivos físicos persistidos e relatório de materialização (`MaterializationResult`)

## Integrations
- [[Generated Projects]]

## Failure behavior
Lança erro de sandbox ou permissão caso ocorra tentativa de escrita fora da pasta de projetos.
