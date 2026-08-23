import logging
import ast
import os
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.e_mcp.mcp_executor import MCPExecutor
from .code_materializer import CodeMaterializer

logger = logging.getLogger(__name__)

class TestMaterializer:
    def __init__(self, mcp: MCPExecutor):
        self.mcp = mcp
        self.code_materializer = CodeMaterializer(mcp)

    def validate_test(self, artifact: Artifact) -> bool:
        # Verifica sintaxe básica
        if artifact.name.endswith(".py"):
            if not self.code_materializer.validate_syntax(artifact.content):
                return False
                
            # Verifica se importa algo de teste (opcional/aviso)
            if "import pytest" not in artifact.content and "import unittest" not in artifact.content:
                logger.warning(f"[TestMaterializer] O arquivo {artifact.name} parece ser um teste mas não importa pytest ou unittest.")
                
            # Verifica nomenclatura se está na raiz dos testes
            basename = os.path.basename(artifact.name)
            if basename.endswith(".py") and not basename.startswith("test_") and basename != "conftest.py" and basename != "__init__.py":
                logger.warning(f"[TestMaterializer] O arquivo {artifact.name} não segue a nomenclatura 'test_*.py'.")
                
        return True
            
    def materialize(self, artifact: Artifact, project_dir: str) -> bool:
        if not self.validate_test(artifact):
            logger.error(f"[TestMaterializer] Falha na validação do teste: {artifact.name}")
            return False
            
        file_path = os.path.join(project_dir, artifact.name)
        res = self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=artifact.content)
        
        if res.get("success"):
            logger.info(f"[TestMaterializer] Teste materializado com sucesso: {artifact.name}")
            return True
        else:
            logger.error(f"[TestMaterializer] Falha ao escrever {artifact.name}: {res.get('error')}")
            return False
