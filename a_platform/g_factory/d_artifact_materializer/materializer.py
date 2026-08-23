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
    Garante que todos os arquivos obrigatórios do projeto sejam escritos baseando-se estritamente no ProjectPlan.
    """
    def __init__(self, mcp: MCPExecutor):
        self.mcp = mcp

    def materialize(self, request: ProjectRequest, artifacts: List[Artifact]) -> bool:
        if not artifacts:
            logger.error("[ArtifactMaterializer] Nenhum artefato recebido para materialização.")
            return False
            
        plan = request.project_plan
        if not plan:
            logger.error("[ArtifactMaterializer] ProjectPlan não encontrado. Não é possível validar a materialização.")
            return False
            
        domain = request.discovery_data.get("domain", "generic").lower()
        project_dir = os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id)
        
        logger.info(f"[ArtifactMaterializer] Iniciando materialização em: {project_dir}")
        
        # Agrupa os artefatos esperados pelo plano
        expected_files = set()
        for task in plan.tasks:
            for art in task.expected_artifacts:
                expected_files.add(art)
                
        # requirements.txt é esperado globalmente (a Factory sempre tenta gerar)
        expected_files.add("requirements.txt")
        
        written_files = set()
        
        for artifact in artifacts:
            file_path = os.path.join(project_dir, artifact.name)
            res = self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=artifact.content)
            if res.get("success"):
                written_files.add(artifact.name)
                logger.info(f"[ArtifactMaterializer] Escrito: {artifact.name}")
            else:
                logger.error(f"[ArtifactMaterializer] Falha ao escrever {artifact.name}: {res.get('error')}")
                
        # Validação estrita
        missing_files = expected_files - written_files
        
        if not missing_files:
            logger.info("[ArtifactMaterializer] Materialização concluída com sucesso. Todos os artefatos esperados foram gravados.")
            return True
        else:
            logger.error(f"[ArtifactMaterializer] FALHA NA MATERIALIZAÇÃO. Artefatos ausentes: {missing_files}")
            return False
