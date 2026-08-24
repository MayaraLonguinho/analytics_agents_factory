import logging
import os
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.e_mcp.mcp_executor import MCPExecutor

logger = logging.getLogger(__name__)

class DocumentationMaterializer:
    def __init__(self, mcp: MCPExecutor):
        self.mcp = mcp

    def validate_doc(self, content: str) -> bool:
        if not content or len(content.strip()) < 10:
            logger.error("[DocumentationMaterializer] Arquivo de documentação vazio ou muito curto.")
            return False
            
        if "TODO" in content or "[MOCK]" in content:
            logger.warning("[DocumentationMaterializer] Documentação contém blocos TODO ou MOCK. Sendo permissivo, mas preste atenção.")
            
        return True
            
    def materialize(self, artifact: Artifact, project_dir: str) -> bool:
        if artifact.name.endswith(".md") or artifact.name.endswith(".txt"):
            if not self.validate_doc(artifact.content):
                logger.error(f"[DocumentationMaterializer] Falha na validação do documento: {artifact.name}")
                return False
                
        file_path = os.path.join(project_dir, artifact.name)
        res = self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=artifact.content)
        
        if res.get("success"):
            logger.info(f"[DocumentationMaterializer] Documentação materializada com sucesso: {artifact.name}")
            return True
        else:
            logger.error(f"[DocumentationMaterializer] Falha ao escrever {artifact.name}: {res.get('error')}")
            return False
