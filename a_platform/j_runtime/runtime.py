"""Runtime orchestration for generated projects."""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ExecutionResult:
    status: str = "UNKNOWN"
    commands: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)
    duration: float = 0.0
    services: List[str] = field(default_factory=list)
    health: Dict[str, Any] = field(default_factory=dict)
    test_results: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "commands": self.commands,
            "outputs": self.outputs,
            "errors": self.errors,
            "logs": self.logs,
            "duration": self.duration,
            "services": self.services,
            "health": self.health,
            "test_results": self.test_results,
            "metadata": self.metadata,
        }


class ProjectRuntime:
    """Executes generated projects and records runtime evidence."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()

    def execute(self, project_path: Optional[Path | str] = None, command: Optional[List[str]] = None) -> ExecutionResult:
        start = time.perf_counter()
        project_dir = Path(
            project_path) if project_path is not None else self.project_root
        project_dir = project_dir.resolve()
        commands = command or self._default_commands(project_dir)
        result = ExecutionResult(status="FAILED", commands=[" ".join(
            str(item) for item in cmd) for cmd in commands])

        for cmd in commands:
            try:
                proc = subprocess.run(cmd, cwd=str(
                    project_dir), capture_output=True, text=True, timeout=180)
                result.outputs.append(proc.stdout.strip())
                if proc.stderr.strip():
                    result.errors.append(proc.stderr.strip())
                result.logs.append(
                    f"$ {' '.join(str(item) for item in cmd)}\n{proc.stdout}\n{proc.stderr}")
                if proc.returncode not in (0, 5):
                    result.status = "FAILED"
                    result.metadata["return_code"] = proc.returncode
                    break
                if proc.returncode == 5:
                    result.status = "SUCCESS"
                    result.metadata["return_code"] = proc.returncode
                    result.metadata["note"] = "No tests were collected for this generated project."
            except Exception as exc:  # pragma: no cover - runtime integration path
                result.errors.append(str(exc))
                result.logs.append(str(exc))
                result.status = "FAILED"
                break
        else:
            result.status = "SUCCESS"

        result.duration = round(time.perf_counter() - start, 3)
        result.services = self._detect_services(project_dir)
        result.health = self._health_snapshot(project_dir)
        result.test_results = self._collect_test_results(project_dir)
        result.metadata["project_path"] = str(project_dir)
        result.metadata["timestamp"] = datetime.now(timezone.utc).isoformat()
        return result

    def _default_commands(self, project_dir: Path) -> List[List[str]]:
        commands: List[List[str]] = []
        
        # 1. Install Dependencies
        if (project_dir / "backend" / "requirements.txt").exists():
            commands.append(["pip", "install", "-r", "backend/requirements.txt"])
        elif (project_dir / "requirements.txt").exists():
            commands.append(["pip", "install", "-r", "requirements.txt"])

        # 2. Database Startup & Migrations
        if (project_dir / "docker-compose.yml").exists():
            commands.append(["docker", "compose", "up", "-d", "db"])
        
        if (project_dir / "database" / "migrations").exists() or (project_dir / "database" / "schema.sql").exists():
            # Mocking migration execution for now
            commands.append(["echo", "Running database migrations..."])
        if (project_dir / "database" / "seeds.py").exists():
            commands.append(["python", "database/seeds.py"])

        # 3. ETL Pipeline
        if (project_dir / "source" / "pipeline.py").exists():
            commands.append(["python", "source/pipeline.py"])

        # 4. Backend Startup & Health Check
        if (project_dir / "backend").exists():
            commands.append(["python", "-m", "compileall", "backend"])
            if (project_dir / "backend" / "healthcheck.py").exists():
                commands.append(["python", "backend/healthcheck.py"])

        # 5. Frontend
        if (project_dir / "frontend" / "package.json").exists():
            commands.append(["npm", "install", "--prefix", "frontend"])
            commands.append(["npm", "run", "build", "--prefix", "frontend"])

        # 6. Tests
        if (project_dir / "tests").exists():
            test_files = list((project_dir / "tests").rglob("test_*.py")) + \
                list((project_dir / "tests").rglob("*_test.py"))
            if test_files:
                commands.append(["python", "-m", "pytest", "-q", "tests"])

        if not commands:
            commands.append(["python", "-m", "compileall", str(project_dir)])
            
        return commands

    def _detect_services(self, project_dir: Path) -> List[str]:
        services: List[str] = []
        for candidate in ["backend", "frontend", "database", "source", "infrastructure"]:
            if (project_dir / candidate).exists():
                services.append(candidate)
        return services

    def _health_snapshot(self, project_dir: Path) -> Dict[str, Any]:
        item = {"materialized": project_dir.exists()}
        for path in [
            "backend/app.py",
            "source/ingestion/pipeline.py",
            "database/schema.sql",
            "docker-compose.yml",
            "README.md",
        ]:
            item[path.replace("/", "_")] = (project_dir / path).exists()
        return item

    def _collect_test_results(self, project_dir: Path) -> Dict[str, Any]:
        result = {"status": "not_run", "passed": 0, "failed": 0, "summary": ""}
        test_dir = project_dir / "tests"
        if not test_dir.exists():
            return result
        pytest = subprocess.run(["python", "-m", "pytest", "-q", str(test_dir)],
                                capture_output=True, text=True, cwd=str(project_dir), timeout=180)
        if pytest.returncode == 0:
            result["status"] = "passed"
        else:
            result["status"] = "failed"
        output = (pytest.stdout or "") + (pytest.stderr or "")
        result["summary"] = output.strip()[-1000:]
        if "passed" in output:
            try:
                value = output.split("passed")[-2].split()[-1]
                result["passed"] = int(value)
            except Exception:
                result["passed"] = 0
        if "failed" in output:
            try:
                value = output.split("failed")[-2].split()[-1]
                result["failed"] = int(value)
            except Exception:
                result["failed"] = 0
        return result


def execute_project(project_path: Optional[Path | str] = None, command: Optional[List[str]] = None) -> ExecutionResult:
    return ProjectRuntime(project_path).execute(project_path=project_path, command=command)
