"""Data engineering domain materializer."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Mapping

from a_platform.h_factory.artifact_materializer.code_materializer import CodeMaterializer
from a_platform.h_factory.artifact_materializer.database_materializer import DatabaseMaterializer
from a_platform.h_factory.artifact_materializer.documentation_materializer import DocumentationMaterializer
from a_platform.h_factory.artifact_materializer.infrastructure_materializer import InfrastructureMaterializer
from a_platform.h_factory.bundle import ProjectGenerationBundle


class DataEngineeringProjectMaterializer:
    def __init__(self, output_dir: Path | str, bundle: ProjectGenerationBundle, project_plan: Mapping[str, Any] | Any):
        self.output_dir = Path(output_dir)
        self.bundle = bundle
        self.project_plan = project_plan
        self.code_materializer = CodeMaterializer(self.output_dir, bundle.domain, generated_by="data_engineering_materializer")
        self.database_materializer = DatabaseMaterializer(self.output_dir, bundle.domain, generated_by="data_engineering_materializer")
        self.documentation_materializer = DocumentationMaterializer(self.output_dir, bundle.domain, generated_by="data_engineering_materializer")
        self.infrastructure_materializer = InfrastructureMaterializer(self.output_dir, bundle.domain, generated_by="data_engineering_materializer")

    def materialize(self) -> List[dict]:
        project_name = self.bundle.project_name
        domain = self.bundle.domain
        stack = dict(self.bundle.stack)
        requires_backend = bool(self.bundle.architecture.get("layers", {}).get("backend"))
        requires_frontend = bool(self.bundle.architecture.get("layers", {}).get("frontend"))
        containerized = bool(self.bundle.architecture.get("infrastructure", {}).get("containerization", True))

        artifacts: List[dict] = []
        artifacts.extend([
            self.code_materializer.create_file("source/ingestion/pipeline.py", self._ingestion_pipeline(), source="data_engineering_materializer", dependencies=["source"], validation_requirements=["ingestion_pipeline_valid"]),
            self.code_materializer.create_file("source/transformation/transform.py", self._transformation_pipeline(), source="data_engineering_materializer", dependencies=["source/ingestion/pipeline.py"], validation_requirements=["transformation_valid"]),
            self.code_materializer.create_file("source/storage/warehouse.py", self._storage(), source="data_engineering_materializer", dependencies=["source/transformation/transform.py"], validation_requirements=["storage_valid"]),
            self.code_materializer.create_file("source/analytics/reporting.py", self._analytics_reporting(), source="data_engineering_materializer", dependencies=["source/storage/warehouse.py"], validation_requirements=["analytics_outputs_valid"]),
            self.code_materializer.create_file("source/visualization/dashboard.py", self._dashboard(), source="data_engineering_materializer", dependencies=["source/analytics/reporting.py"], validation_requirements=["dashboard_valid"]),
        ])
        artifacts.extend(self.database_materializer.generate(domain, project_name, include_seeds=True))
        if requires_backend:
            artifacts.append(self.code_materializer.create_file("backend/app.py", self._backend_app(), source="data_engineering_materializer", dependencies=["source/analytics/reporting.py"], validation_requirements=["backend_starts"]))
        if requires_frontend:
            artifacts.append(self.code_materializer.create_file("frontend/src/App.tsx", self._frontend_app(), source="data_engineering_materializer", dependencies=["backend/app.py"], validation_requirements=["frontend_builds"]))
        artifacts.extend(self.infrastructure_materializer.generate(domain, project_name, containerized=containerized, include_terraform=bool(self.bundle.runtime_config.get("terraform"))))
        artifacts.extend(self.documentation_materializer.generate(domain, project_name, stack, requires_backend, requires_frontend))
        return artifacts

    @staticmethod
    def _ingestion_pipeline() -> str:
        return """from typing import Iterable


def ingest(rows: Iterable[dict]) -> list[dict]:
    return [dict(row) for row in rows]
"""

    @staticmethod
    def _transformation_pipeline() -> str:
        return """from typing import Iterable


def transform(rows: Iterable[dict]) -> list[dict]:
    return [{**row, "normalized": True} for row in rows]
"""

    @staticmethod
    def _storage() -> str:
        return """class Warehouse:
    def __init__(self):
        self.tables = {}

    def add(self, table: str, rows: list[dict]):
        self.tables[table] = rows
"""

    @staticmethod
    def _analytics_reporting() -> str:
        return """from typing import Iterable


def summarize(rows: Iterable[dict]) -> dict:
    return {"count": len(list(rows)), "status": "ok"}
"""

    @staticmethod
    def _dashboard() -> str:
        return """def dashboard_config():
    return {"title": "Generated Dashboard", "widgets": []}
"""

    @staticmethod
    def _backend_app() -> str:
        return """from fastapi import FastAPI

app = FastAPI(title='Data Engineering API')


@app.get('/health')
async def health():
    return {'status': 'ok'}
"""

    @staticmethod
    def _frontend_app() -> str:
        return """import React from 'react';

export default function App() {
  return <div>Data engineering frontend</div>;
}
"""


__all__ = ["DataEngineeringProjectMaterializer"]
