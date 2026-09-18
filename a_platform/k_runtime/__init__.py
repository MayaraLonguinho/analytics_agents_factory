"""Runtime package for generated projects."""

from .a_execution.a_runtime import ExecutionResult, ProjectRuntime

__all__ = ["ExecutionResult", "ProjectRuntime", "execute_project"]
