import logging
import re
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.f_mcp.mcp_executor import MCPExecutor

logger = logging.getLogger(__name__)

class DatabaseMaterializer:
    def __init__(self, mcp: MCPExecutor):
        self.mcp = mcp

    def validate_sql(self, content: str) -> bool:
        if not content or len(content.strip()) < 5:
            logger.error("[DatabaseMaterializer] Script SQL muito curto ou vazio.")
            return False
            
        mock_patterns = [r'\[MOCK', r'mocked data', r'# TODO: add sql']
        for pattern in mock_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                logger.error("[DatabaseMaterializer] Artefato SQL contém strings de mock explícitas.")
                return False
                
        # Basic check for SQL keywords
        sql_keywords = ['CREATE', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'ALTER', 'DROP']
        if not any(kw in content.upper() for kw in sql_keywords):
            logger.warning("[DatabaseMaterializer] O script SQL não contém palavras-chave comuns. Permitindo mesmo assim...")
            
        return True
            
    def materialize(self, artifact: Artifact, project_dir: str) -> bool:
        if artifact.name.endswith(".sql"):
            if not self.validate_sql(artifact.content):
                logger.error(f"[DatabaseMaterializer] Falha na validação do SQL: {artifact.name}")
                return False
                
        import os
        file_path = os.path.join(project_dir, artifact.name)
        res = self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=artifact.content)
        
        if res.get("success"):
            logger.info(f"[DatabaseMaterializer] Script de banco de dados materializado com sucesso: {artifact.name}")
            return True
        else:
            logger.error(f"[DatabaseMaterializer] Falha ao escrever {artifact.name}: {res.get('error')}")
            return False
