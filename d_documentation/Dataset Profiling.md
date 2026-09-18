# Dataset Profiling

## Responsibility
Análise estática do arquivo físico de dados (via Pandas) para extração determinística de contagem de linhas, colunas, esquemas de dados, duplicatas e avisos estruturais.

## Path
`a_platform/e_skills/a_dataset_profiling/c_profiling/a_profiler.py`

## Inputs
[[Discovery]], [[Orchestrator]]

## Outputs
DatasetProfile (`row_count`, `column_count`, `columns`, `duplicate_rows`, `warnings`)

## Integrations
- [[Brain]]

## Failure behavior
Registra alertas estruturais no contexto ou falha a esteira caso o arquivo seja inacessível ou corrompido.
