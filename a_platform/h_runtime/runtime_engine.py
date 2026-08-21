from a_platform.h_runtime.docker_controller import DockerController
from a_platform.h_runtime.health_checker import HealthChecker

class RuntimeEngine:
    def __init__(self):
        self.docker = DockerController()
        self.health = HealthChecker()

    def run_project(self, project_dir: str, check_url: str = "http://localhost:8000/health") -> bool:
        success = self.docker.build_and_up(project_dir)
        if success:
            return self.health.check_health(check_url)
        return False
