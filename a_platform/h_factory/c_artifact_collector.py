import logging
from typing import List
from a_platform.b_contracts import Artifact, ProjectTask

logger = logging.getLogger(__name__)

class ArtifactCollector:
    @staticmethod
    def collect(plan: List[ProjectTask], agents_output: List[Artifact]) -> List[Artifact]:
        expected_files = set()
        for task in plan:
            for art in getattr(task, "expected_artifacts", []):
                expected_files.add(art)
                
        generated_files = {art.path for art in agents_output}
        missing = expected_files - generated_files
        
        if "requirements.txt" in missing and "requirements.txt" not in [art for task in plan for art in getattr(task, "expected_artifacts", [])]:
            missing.remove("requirements.txt")
            
        if missing:
            logger.warning(f"[ArtifactCollector] Artefatos planejados não foram gerados: {missing}")
            
        return agents_output
