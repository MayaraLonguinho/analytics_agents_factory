"""Project Factory - End-to-end project generation.

This package keeps imports lazy so core generation modules can be imported
without pulling in the full runtime/orchestrator stack during package init.
"""

__all__ = [
    "ProjectGenerationBundle",
    "ProjectTask",
    "ProjectPlanner",
    "ProjectFactory",
    "ProjectGenerationPipeline",
]


def __getattr__(name):
    if name in {"ProjectGenerationBundle", "ProjectTask"}:
        from .bundle import ProjectGenerationBundle, ProjectTask
        return {"ProjectGenerationBundle": ProjectGenerationBundle, "ProjectTask": ProjectTask}[name]
    if name == "ProjectPlanner":
        from .planner import ProjectPlanner
        return ProjectPlanner
    if name in {"ProjectFactory", "ProjectGenerationPipeline"}:
        from .factory import ProjectFactory, ProjectGenerationPipeline
        return {"ProjectFactory": ProjectFactory, "ProjectGenerationPipeline": ProjectGenerationPipeline}[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
