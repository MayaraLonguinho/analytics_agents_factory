import logging
import os
from typing import List, Set

from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts import Artifact
from a_platform.f_mcps.d_registry.b_executor import MCPExecutor
from .c_artifact_writer import ArtifactWriter
from .d_materialization_result import MaterializationResult

logger = logging.getLogger(__name__)

class ArtifactMaterializer:
    def __init__(self, mcp: MCPExecutor):
        self.writer = ArtifactWriter(mcp)

    def materialize(self, request: ExecutionContext, artifacts: List[Artifact]) -> MaterializationResult:
        if not artifacts:
            return MaterializationResult(status="FAILED", evidence="No artifacts to materialize")
            
        plan = getattr(request.project_context, "plan", [])
        if not plan:
            return MaterializationResult(status="FAILED", evidence="No project plan in ProjectContext")
            
        project_dir = request.project_context.project_path
        if not project_dir:
            return MaterializationResult(status="FAILED", evidence="Project path is not defined in ProjectContext")
            
        logger.info(f"[ArtifactMaterializer] Iniciando materialização em: {project_dir}")
        
        expected_files = set()
        for task in plan:
            for art in getattr(task, "expected_artifacts", []):
                expected_files.add(art)
                
        # Group artifacts by capability based on metadata, default to "generic"
        capability_map = {}
        for art in artifacts:
            cap = art.metadata.get("capability", "generic") if art.metadata else "generic"
            capability_map.setdefault(cap, []).append(art)
            
        all_written = []
        all_errors = []
        
        for cap, arts in capability_map.items():
            logger.info(f"Materializando capability: {cap}")
            res = self.writer.write_artifacts(project_dir, cap, arts)
            all_written.extend(res["written"])
            all_errors.extend(res["errors"])
            
        written_files = set(all_written)
        missing_files = expected_files - written_files
        
        if "requirements.txt" in missing_files and "requirements.txt" not in [art for task in plan for art in getattr(task, "expected_artifacts", [])]:
            missing_files.remove("requirements.txt")
            
        if all_errors or missing_files:
            error_msg = f"Artefatos ausentes/falhos: {missing_files} | {all_errors}"
            logger.error(f"[ArtifactMaterializer] {error_msg}")
            return MaterializationResult(
                status="FAILED",
                evidence="Materialization failed partially or completely",
                errors=list(missing_files) + all_errors,
                materialized_paths=all_written
            )
            
        return MaterializationResult(
            status="PASSED",
            evidence="All expected artifacts materialized successfully",
            materialized_paths=all_written
        )
