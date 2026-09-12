import subprocess

class DockerController:
    def build_and_up(self, project_dir: str) -> bool:
        try:
            # Mock subprocess run logic for building and starting containers
            result = subprocess.run(
                ["docker-compose", "up", "-d", "--build"],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
