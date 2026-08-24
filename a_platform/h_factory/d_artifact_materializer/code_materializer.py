import ast
import logging
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_mcp.mcp_executor import MCPExecutor

logger = logging.getLogger(__name__)

class CodeMaterializer:
    def __init__(self, mcp: MCPExecutor):
        self.mcp = mcp

    def validate_syntax(self, content: str) -> bool:
        try:
            ast.parse(content)
            return True
        except SyntaxError as e:
            logger.error(f"[CodeMaterializer] Erro de sintaxe detectado: {e}")
            return False
            
    def materialize(self, artifact: Artifact, project_dir: str) -> bool:
        if artifact.name.endswith(".py"):
            if not self.validate_syntax(artifact.content):
                logger.error(f"[CodeMaterializer] Falha na validação sintática do artefato: {artifact.name}")
                return False
                
        # Usa o MCP para escrever o arquivo
        import os
        file_path = os.path.join(project_dir, artifact.name)
        res = self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=artifact.content)
        
        if res.get("success"):
            logger.info(f"[CodeMaterializer] Código materializado com sucesso: {artifact.name}")
            return True
        else:
            logger.error(f"[CodeMaterializer] Falha ao escrever {artifact.name}: {res.get('error')}")
            return False
