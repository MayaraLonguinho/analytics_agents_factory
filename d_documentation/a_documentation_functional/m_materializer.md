# Materializer

## Papel no Golden Path
Responsável pela gravação física atômica dos artefatos em disco. Aplica a política de caminhos seguros (`PathPolicy`) para impedir qualquer tentativa de *path traversal* (como uso de `..` para escapar do diretório do projeto), utiliza o MCP de filesystem e confere se todos os arquivos esperados foram de fato persistidos.

## Posição no Fluxo
← **Anterior:** [[l_artifact|Artifact]]  
→ **Próximo:** [[n_generated_projects|Generated Projects]]

## Entrada e Saída
- **Entrada:** Lista de `Artifact` compilados e caminho raiz do projeto (`request.project_context.project_path`).
- **Saída:** `MaterializationResult` com status (`PASSED`/`FAILED`), caminhos materializados e atualização de `materialization_status = "SUCCESS"`.

## Integrações e Contratos
- Componente: `a_platform/i_materializer/a_materializer.py` (`ArtifactMaterializer`)
- Política de Caminhos: `a_platform/i_materializer/b_path_policy.py` (`PathPolicy`)
- Escritor: `a_platform/i_materializer/c_artifact_writer.py`

## Referência Técnica
Para detalhes do isolamento do disco e regras de escrita, consulte [[a_architecture|Arquitetura Geral]].
