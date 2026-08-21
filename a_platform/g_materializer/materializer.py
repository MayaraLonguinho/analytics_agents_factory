import os
from typing import List
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.g_materializer.file_system import FileSystemOps
from a_platform.g_materializer.formatters import format_content

class Materializer:
    def __init__(self, base_dir: str = "e_generated_projects"):
        self.base_dir = base_dir

    def materialize(self, project_id: str, artifacts: List[Artifact]) -> str:
        project_dir = os.path.join(self.base_dir, project_id)
        FileSystemOps.ensure_directory(project_dir)
        
        for artifact in artifacts:
            file_path = os.path.join(project_dir, artifact.path)
            # Ensure subdirectories exist for the artifact
            FileSystemOps.ensure_directory(os.path.dirname(file_path))
            
            formatted_content = format_content(artifact.path, artifact.content)
            FileSystemOps.write_file(file_path, formatted_content)
            
        return project_dir
