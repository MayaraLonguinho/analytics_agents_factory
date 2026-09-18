# Generated Projects

## Papel no Golden Path
Diretório raiz exclusivo e isolado para armazenamento dos projetos analíticos gerados pela plataforma. Cada projeto reside estritamente em uma subpasta identificada pelo seu ID (`e_generated_projects/<project_id>/`). Antes de qualquer execução, a pasta raiz mantém apenas `.gitkeep`, garantindo ambiente limpo.

## Posição no Fluxo
← **Anterior:** [[m_materializer|Materializer]]  
→ **Próximo:** [[o_runtime|Runtime]]

## Entrada e Saída
- **Entrada:** Artefatos físicos gravados pelo `ArtifactMaterializer`.
- **Saída:** Árvore de arquivos completa e executável do projeto analítico gerado.

## Integrações e Contratos
- Localização Física: `e_generated_projects/<project_id>/`
- Proteção: `PathPolicy` garante que nenhum arquivo seja gravado fora desta árvore.

## Referência Técnica
Para detalhes do isolamento em disco e estrutura dos projetos, consulte [[i_runtime|Mecanismos de Runtime]].
