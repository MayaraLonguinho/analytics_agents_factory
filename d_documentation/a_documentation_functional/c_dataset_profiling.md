# Dataset Profiling

## Papel no Golden Path
Inspeção física direta do arquivo de dados fornecido pelo usuário. A habilidade `DatasetProfilingSkill` lê o arquivo via Pandas puro em disco (CSV ou JSON) para extrair estatísticas reais e schema estruturado, sem utilizar LLM e sem mocks.

## Posição no Fluxo
← **Anterior:** [[b_discovery|Discovery]]  
→ **Próximo:** [[d_brain|Brain]]

## Entrada e Saída
- **Entrada:** `request.dataset_path` (caminho absoluto ou relativo do dataset de entrada).
- **Saída:** `request.dataset_profile` contendo contagem de linhas (`row_count`), colunas (`column_count`), tipos inferidos, porcentagem de nulos e alertas de duplicatas.

## Integrações e Contratos
- Componente: `a_platform/e_skills/a_dataset_profiling/c_profiling/a_profiler.py`
- Contrato base: `BaseSkill` com validação de entrada física e saída estruturada.

## Referência Técnica
Para o catálogo de habilidades e execução de contratos, consulte [[d_skills|Subsistema de Skills]].
