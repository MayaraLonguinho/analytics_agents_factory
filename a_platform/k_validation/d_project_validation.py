"""
ProjectValidation gate.

Checks global coherence of the project context before other gates run:
- project_context and project_id exist
- project_path exists on disk (when set)
- plan is present and non-empty
- materialization_status is SUCCESS (when recorded)
"""
import os
from a_platform.b_contracts.e_execution_context import ExecutionContext


class ProjectValidation:
    def validate(self, request: ExecutionContext) -> bool:
        ctx = request.project_context
        if not ctx:
            return False

        if not request.project_id:
            return False

        # project_path must exist on disk when the context records one
        project_path = getattr(ctx, "project_path", None)
        if project_path and not os.path.isdir(project_path):
            return False

        # Plan must exist and have at least one task
        plan = getattr(ctx, "plan", None)
        if not plan:
            return False

        # If materialization status was recorded it must be SUCCESS
        mat_status = getattr(ctx, "materialization_status", None)
        if mat_status is not None and mat_status != "SUCCESS":
            return False

        return True
