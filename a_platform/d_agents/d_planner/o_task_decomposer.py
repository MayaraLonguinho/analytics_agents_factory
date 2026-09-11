from typing import List

class TaskDecomposer:
    def decompose(self, domain: str) -> List[str]:
        # Simple topological sort DAG representation
        return ["db_setup", "etl_pipeline", "backend_api", "frontend_dashboard", "devops_infra", "qa_tests"]
