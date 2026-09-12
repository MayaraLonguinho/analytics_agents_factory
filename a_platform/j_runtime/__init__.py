"""Runtime package for generated projects."""

from .a_execution.c_runtime import ExecutionResult, ProjectRuntime, execute_project

__all__ = ["ExecutionResult", "ProjectRuntime", "execute_project"]
