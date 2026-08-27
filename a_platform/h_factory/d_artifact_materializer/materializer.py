import logging
import os
from typing import List
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_mcp.mcp_executor import MCPExecutor

from .code_materializer import CodeMaterializer
from .database_materializer import DatabaseMaterializer
from .materializer_test_support import TestMaterializer
from .documentation_materializer import DocumentationMaterializer
from .infrastructure_materializer import InfrastructureMaterializer

logger = logging.getLogger(__name__)

class ArtifactMaterializer:
    """
    Grava os artefatos compilados no sistema de arquivos usando o MCP Executor,
    delegando para materializadores especializados para garantir integridade.
    """
    def __init__(self, mcp: MCPExecutor):
        self.mcp = mcp
        self.code_mat = CodeMaterializer(mcp)
        self.db_mat = DatabaseMaterializer(mcp)
        self.test_mat = TestMaterializer(mcp)
        self.doc_mat = DocumentationMaterializer(mcp)
        self.infra_mat = InfrastructureMaterializer(mcp)

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
                
        # requirements.txt é esperado globalmente
        expected_files.add("requirements.txt")
        
        written_files = set()
        
        for artifact in artifacts:
            name = artifact.name.lower()
            
            # Routing
            if name.endswith(".sql"):
                success = self.db_mat.materialize(artifact, project_dir)
            elif name.startswith("test_") or "test" in name and name.endswith(".py"):
                success = self.test_mat.materialize(artifact, project_dir)
            elif name.endswith(".py"):
                success = self.code_mat.materialize(artifact, project_dir)
            elif name.endswith(".md") or (name.endswith(".txt") and name != "requirements.txt"):
                success = self.doc_mat.materialize(artifact, project_dir)
            elif name.endswith(".json") or name.endswith(".yaml") or name.endswith(".yml") or "dockerfile" in name or name == "requirements.txt":
                success = self.infra_mat.materialize(artifact, project_dir)
            else:
                # Default materialization if not matched
                file_path = os.path.join(project_dir, artifact.name)
                res = self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=artifact.content)
                success = res.get("success", False)
                if not success:
                    logger.error(f"[ArtifactMaterializer] Falha ao escrever {artifact.name}: {res.get('error')}")

            if success:
                written_files.add(artifact.name)
                
        missing_files = expected_files - written_files
        
        # O system_prompt do PlannerAgent geralmente não obriga "requirements.txt" se a task for só DDL, 
        # mas adicionamos estaticamente acima. Para não dar falsos negativos se o plano não gerar requirements, 
        # focaremos na estrita cobrança dos expected_artifacts das tasks.
        if "requirements.txt" in missing_files and "requirements.txt" not in [art for task in plan.tasks for art in task.expected_artifacts]:
            missing_files.remove("requirements.txt")
        
        if not missing_files:
            logger.info("[ArtifactMaterializer] Materialização concluída com sucesso. Todos os artefatos esperados foram gravados.")
            return True
        else:
            logger.error(f"[ArtifactMaterializer] FALHA NA MATERIALIZAÇÃO. Artefatos ausentes: {missing_files}")
            return False
