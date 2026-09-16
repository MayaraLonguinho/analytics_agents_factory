import os
from typing import Dict, Any, List
from a_platform.f_mcps.d_registry.b_executor import MCPExecutor
from a_platform.b_contracts import Artifact
from .b_path_policy import PathPolicy

class ArtifactWriter:
    def __init__(self, mcp: MCPExecutor):
        self.mcp = mcp

    def write_artifacts(self, base_path: str, capability: str, artifacts: List[Artifact]) -> Dict[str, Any]:
        written = []
        errors = []
        for art in artifacts:
            target_path = PathPolicy.resolve_and_verify(base_path, art.path)
            if not target_path:
                errors.append(f"Security violation or invalid path: {art.path}")
                continue
                
            mcp_result = self.mcp.execute(
                "filesystem_mcp",
                payload={
                    "operation": "write",
                    "path": target_path,
                    "content": art.content
                }
            )
            
            if mcp_result.get("status") == "ok":
                written.append(art.path)
            else:
                errors.append(f"Falha ao escrever {art.path}: {mcp_result.get("message")}")
                
        return {"written": written, "errors": errors}
