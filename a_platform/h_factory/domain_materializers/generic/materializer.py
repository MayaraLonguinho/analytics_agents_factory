"""Generic domain materializer."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Mapping

from a_platform.h_factory.artifact_materializer.code_materializer import CodeMaterializer
from a_platform.h_factory.artifact_materializer.database_materializer import DatabaseMaterializer
from a_platform.h_factory.artifact_materializer.documentation_materializer import DocumentationMaterializer
from a_platform.h_factory.artifact_materializer.infrastructure_materializer import InfrastructureMaterializer
from a_platform.h_factory.bundle import ProjectGenerationBundle


class GenericProjectMaterializer:
    """Generic deterministic materializer used when no specific domain logic is needed."""

    def __init__(self, output_dir: Path | str, bundle: ProjectGenerationBundle, project_plan: Mapping[str, Any] | Any):
        self.output_dir = Path(output_dir)
        self.bundle = bundle
        self.project_plan = project_plan
        self.code_materializer = CodeMaterializer(self.output_dir, bundle.domain, generated_by="generic_materializer")
        self.database_materializer = DatabaseMaterializer(self.output_dir, bundle.domain, generated_by="generic_materializer")
        self.documentation_materializer = DocumentationMaterializer(self.output_dir, bundle.domain, generated_by="generic_materializer")
        self.infrastructure_materializer = InfrastructureMaterializer(self.output_dir, bundle.domain, generated_by="generic_materializer")

    def materialize(self) -> List[dict]:
        artifacts: List[dict] = []
        project_name = self.bundle.project_name
        domain = self.bundle.domain
        stack = dict(self.bundle.stack)
        requires_backend = bool(self.bundle.architecture.get("layers", {}).get("backend"))
        requires_frontend = bool(self.bundle.architecture.get("layers", {}).get("frontend"))
        needs_db = bool(self.bundle.runtime_config.get("database") or self.bundle.architecture.get("layers", {}).get("database"))
        containerized = bool(self.bundle.architecture.get("infrastructure", {}).get("containerization", True))

        artifacts.extend(self._generate_source_tree())
        if needs_db:
            artifacts.extend(self.database_materializer.generate(domain, project_name, include_seeds=True))
        artifacts.extend(self.infrastructure_materializer.generate(domain, project_name, containerized=containerized, include_terraform=bool(self.bundle.runtime_config.get("terraform"))))
        artifacts.extend(self.documentation_materializer.generate(domain, project_name, stack, requires_backend, requires_frontend))
        return sorted(artifacts, key=lambda item: item.path)

    def _generate_source_tree(self) -> List[dict]:
        artifacts: List[dict] = []
        if self.bundle.domain in {"analytics", "data_engineering"}:
            artifacts.append(self.code_materializer.create_file(
                "source/ingestion/pipeline.py",
                self._ingestion_pipeline(),
                source="generic_materializer",
                dependencies=["source"],
                validation_requirements=["ingestion_pipeline_valid"],
            ))
            artifacts.append(self.code_materializer.create_file(
                "source/transformation/transform.py",
                self._transformation_pipeline(),
                source="generic_materializer",
                dependencies=["source/ingestion/pipeline.py"],
                validation_requirements=["transformation_valid"],
            ))
            artifacts.append(self.code_materializer.create_file(
                "source/analytics/reporting.py",
                self._analytics_reporting(),
                source="generic_materializer",
                dependencies=["source/transformation/transform.py"],
                validation_requirements=["analytics_outputs_valid"],
            ))
        else:
            artifacts.append(self.code_materializer.create_file(
                "source/app.py",
                self._app_stub(),
                source="generic_materializer",
                dependencies=[],
                validation_requirements=["application_boots"],
            ))

        if self.bundle.architecture.get("layers", {}).get("backend"):
            backend_dir = Path(self.output_dir) / "backend"
            backend_dir.mkdir(parents=True, exist_ok=True)
            artifacts.append(self.code_materializer.create_file(
                "backend/app.py",
                self._backend_stub(),
                source="generic_materializer",
                dependencies=["source/app.py"],
                validation_requirements=["backend_starts"],
            ))
            artifacts.append(self.code_materializer.create_file(
                "backend/requirements.txt",
                "fastapi==0.110.0\nuvicorn==0.29.0\n",
                source="generic_materializer",
                dependencies=["backend/app.py"],
                validation_requirements=["dependency_lock_present"],
            ))

        if self.bundle.architecture.get("layers", {}).get("frontend"):
            artifacts.append(self.code_materializer.create_file(
                "frontend/src/App.tsx",
                self._frontend_stub(),
                source="generic_materializer",
                dependencies=["backend/app.py"],
                validation_requirements=["frontend_builds"],
            ))

        return artifacts

    @staticmethod
    def _ingestion_pipeline() -> str:
        return '''"""Ingestion pipeline."""
from typing import Iterable


def ingest(rows: Iterable[dict]) -> list[dict]:
    return [dict(row) for row in rows]
'''

    @staticmethod
    def _transformation_pipeline() -> str:
        return '''"""Transformation layer."""
from typing import Iterable


def transform(rows: Iterable[dict]) -> list[dict]:
    return [{**row, "normalized": True} for row in rows]
'''

    @staticmethod
    def _analytics_reporting() -> str:
        return '''"""Analytics reporting."""
from typing import Iterable


def summarize(rows: Iterable[dict]) -> dict:
    return {"count": len(list(rows)), "status": "ok"}
'''

    @staticmethod
    def _app_stub() -> str:
        return '''"""Application stub."""
print("Project application ready")
'''

    @staticmethod
    def _backend_stub() -> str:
        return '''"""Backend API stub."""
from fastapi import FastAPI

app = FastAPI(title="Generated API")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
'''

    @staticmethod
    def _frontend_stub() -> str:
        return """import React from 'react';

export default function App() {
  return <div>Generated frontend</div>;
}
"""


