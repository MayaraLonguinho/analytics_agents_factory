import logging
import json
import yaml
import os
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.e_mcp.mcp_executor import MCPExecutor

logger = logging.getLogger(__name__)

class InfrastructureMaterializer:
    def __init__(self, mcp: MCPExecutor):
        self.mcp = mcp

    def validate_infra(self, artifact: Artifact) -> bool:
        content = artifact.content
        name = artifact.name.lower()
        
        if not content or len(content.strip()) < 5:
            logger.error(f"[InfrastructureMaterializer] Arquivo infra vazio ou muito curto: {name}")
            return False
            
        if name.endswith(".json"):
            try:
                json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"[InfrastructureMaterializer] JSON inválido em {name}: {e}")
                return False
                
        elif name.endswith(".yaml") or name.endswith(".yml"):
            try:
                yaml.safe_load(content)
            except yaml.YAMLError as e:
                logger.error(f"[InfrastructureMaterializer] YAML inválido em {name}: {e}")
                return False
                
        # Para Dockerfile, não temos validador nativo estrito, vamos buscar FROM
        elif "dockerfile" in name:
            if "FROM " not in content:
                logger.error(f"[InfrastructureMaterializer] Dockerfile não possui instrução FROM: {name}")
                return False
                
        return True
            
    def materialize(self, artifact: Artifact, project_dir: str) -> bool:
        if not self.validate_infra(artifact):
            logger.error(f"[InfrastructureMaterializer] Falha na validação de infra: {artifact.name}")
            return False
            
        file_path = os.path.join(project_dir, artifact.name)
        res = self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=artifact.content)
        
        if res.get("success"):
            logger.info(f"[InfrastructureMaterializer] Infraestrutura materializada com sucesso: {artifact.name}")
            return True
        else:
            logger.error(f"[InfrastructureMaterializer] Falha ao escrever {artifact.name}: {res.get('error')}")
            return False
