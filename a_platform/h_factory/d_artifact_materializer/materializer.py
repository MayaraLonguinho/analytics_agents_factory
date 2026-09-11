import logging
import os
from typing import List
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_mcp.mcp_executor import MCPExecutor

logger = logging.getLogger(__name__)

class ArtifactMaterializer:
    """
    Grava os artefatos compilados no sistema de arquivos usando o MCP Executor.
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
            
        domain = request.discovery_data.get("domain", "analytics").lower()
        project_dir = os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id)
        
        logger.info(f"[ArtifactMaterializer] Iniciando materialização em: {project_dir}")
        
        expected_files = set()
        for task in plan.tasks:
            for art in task.expected_artifacts:
                expected_files.add(art)
                
        expected_files.add("requirements.txt")
        written_files = set()
        
        for artifact in artifacts:
            file_path = os.path.join(project_dir, artifact.name)
            res = self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=artifact.content)
            success = res.get("success", False)
            if not success:
                logger.error(f"[ArtifactMaterializer] Falha ao escrever {artifact.name}: {res.get('error')}")
            else:
                written_files.add(artifact.name)
                
        missing_files = expected_files - written_files
        
        if "requirements.txt" in missing_files and "requirements.txt" not in [art for task in plan.tasks for art in task.expected_artifacts]:
            missing_files.remove("requirements.txt")
        
        physically_missing = set()
        for expected_file in expected_files:
            if expected_file == "requirements.txt" and "requirements.txt" not in [art for task in plan.tasks for art in task.expected_artifacts]:
                continue
            file_path = os.path.join(project_dir, expected_file)
            if not os.path.exists(file_path):
                physically_missing.add(expected_file)
        
        if missing_files or physically_missing:
            logger.error(f"[ArtifactMaterializer] FALHA NA MATERIALIZAÇÃO. Artefatos ausentes logicamente: {missing_files}. Artefatos ausentes fisicamente no disco: {physically_missing}")
            return False

        logger.info("[ArtifactMaterializer] Materialização concluída com sucesso. Todos os artefatos esperados foram gravados e validados fisicamente no disco.")
        return True
