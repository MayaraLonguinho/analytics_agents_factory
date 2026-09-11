"""
Planner Agent - Agente especializado em planejamento de execução
"""

from .i_schemas import (
    # Enums
    TaskStatus,
    TaskPriority,
    TaskType,

    # Task schemas
    Task,

    # DAG schemas
    DirectedAcyclicGraph,

    # Parallel group schemas
    ParallelGroup,

    # Cost estimation schemas
    CostEstimate,

    # Execution plan schemas
    ExecutionPlan,

    # Planning context schemas
    PlanningContext,
    PlanningRequest,
    PlanningResult
)

from .f_interfaces import (
    IPlanner,
    ITaskDecomposer,
    IDAGGenerator,
    IDependencyResolver,
    IParallelismDetector,
    ICostEstimator,
    IAgentAssigner,
    IPriorityManager
)

from .h_planner import PlannerAgent

__version__ = "1.0.0"

__all__ = [
    # Enums
    "TaskStatus",
    "TaskPriority",
    "TaskType",

    # Schemas
    "Task",
    "DirectedAcyclicGraph",
    "ParallelGroup",
    "CostEstimate",
    "ExecutionPlan",
    "PlanningContext",
    "PlanningRequest",
    "PlanningResult",

    # Interfaces
    "IPlanner",
    "ITaskDecomposer",
    "IDAGGenerator",
    "IDependencyResolver",
    "IParallelismDetector",
    "ICostEstimator",
    "IAgentAssigner",
    "IPriorityManager",

    # Implementation
    "PlannerAgent",

    # Version
    "__version__"
]
