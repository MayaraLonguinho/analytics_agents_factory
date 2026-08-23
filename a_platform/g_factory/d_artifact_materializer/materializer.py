import logging
import os
from typing import List
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.e_mcp.mcp_executor import MCPExecutor

logger = logging.getLogger(__name__)

class ArtifactMaterializer:
    """
    Grava os artefatos compilados no sistema de arquivos usando o MCP Executor.
    Garante que todos os arquivos obrigatórios do projeto sejam escritos.
    """
    def __init__(self, mcp: MCPExecutor):
        self.mcp = mcp

    def materialize(self, request: ProjectRequest, artifacts: List[Artifact]) -> bool:
        if not artifacts:
            logger.error("[ArtifactMaterializer] Nenhum artefato recebido para materialização.")
            return False
            
        domain = request.discovery_data.get("domain", "generic").lower()
        project_dir = os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id)
        
        logger.info(f"[ArtifactMaterializer] Iniciando materialização em: {project_dir}")
        success_count = 0
        
        for artifact in artifacts:
            file_path = os.path.join(project_dir, artifact.name)
            res = self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=artifact.content)
            if res.get("success"):
                success_count += 1
                logger.info(f"[ArtifactMaterializer] Escrito: {artifact.name}")
            else:
                logger.error(f"[ArtifactMaterializer] Falha ao escrever {artifact.name}: {res.get('error')}")
                
        # Materialization = SUCCESS se pelo menos a maior parte for escrita.
        # Aqui podemos aplicar regras estritas (ex: success_count == len(artifacts))
        if success_count == len(artifacts):
            logger.info("[ArtifactMaterializer] Todos os artefatos gravados com sucesso.")
            return True
        else:
            logger.error(f"[ArtifactMaterializer] Apenas {success_count} de {len(artifacts)} artefatos foram escritos.")
            return False
