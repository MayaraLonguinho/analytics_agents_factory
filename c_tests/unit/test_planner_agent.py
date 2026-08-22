import pytest
from a_platform.c_agents.d_planner.planner_agent import PlannerAgent
from a_platform.a_core.b_domain.project_plan import ProjectPlan

@pytest.mark.asyncio
async def test_planner_agent_execute():
    agent = PlannerAgent()
    plan = ProjectPlan(project_id="test", name="test", domain="generic")
    result = await agent.execute(plan)
    assert len(result.tasks) == 6
    assert result.tasks[0] == "db_setup"
    assert result.tasks[-1] == "qa_tests"
