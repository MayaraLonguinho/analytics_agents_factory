from typing import Optional
from a_platform.a_core.b_domain.project_plan import ProjectPlan
from a_platform.f_llm_gateway.gateway import LLMGateway
from a_platform.c_agents.d_planner.task_decomposer import TaskDecomposer

class PlannerAgent:
    def __init__(self, gateway: Optional[LLMGateway] = None):
        self.gateway = gateway or LLMGateway()
        self.decomposer = TaskDecomposer()

    async def execute(self, plan: ProjectPlan) -> ProjectPlan:
        tasks = self.decomposer.decompose(plan.domain)
        plan.tasks = tasks
        return plan
