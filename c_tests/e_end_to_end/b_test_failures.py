import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

import os
import shutil
from unittest.mock import patch
from a_platform.n_orchestration.a_orchestrator import MasterOrchestrator
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.a_core.a_contracts.d_project_contract import ProjectPlan, ProjectTask
from a_platform.g_llm_gateway.f_interfaces.a_base_provider import LLMResponse

@patch("a_platform.g_llm_gateway.e_gateway.LLMGateway.structured_output")
@patch("a_platform.g_llm_gateway.e_gateway.LLMGateway.generate")
@patch("a_platform.d_agents.c_planner.k_planner_agent.PlannerAgent.generate_plan")
def test_execution_failure_blocks_readiness(mock_planner, mock_generate, mock_structured):
    mock_generate.return_value = LLMResponse(content='{"domain": "mock_domain", "patterns": []}', model="mock", provider="mock")
    mock_structured.return_value = LLMResponse(content='{"architecture": "mock"}', model="mock", provider="mock")
    
    def side_effect_plan(request):
        request.project_plan = ProjectPlan(
            project_id=request.project_id,
            tasks=[ProjectTask(task_id="t1", name="Create app", assigned_agent="DataAgent")]
        )
        return True
    mock_planner.side_effect = side_effect_plan

    orchestrator = MasterOrchestrator()
    
    ctx = ExecutionContext(
        project_id="test_fail_exec", 
        prompt="Fail app", 
        domain="analytics",
        discovery_data={"domain": "analytics"}
    )
    
    from a_platform.a_core.a_contracts.e_execution_contract import ExecutionResult
    with patch("a_platform.j_runtime.a_execution.c_runtime.ProjectRuntime.execute", return_value=ExecutionResult(task_id="t1", success=False, error="SyntaxError")):
        result = orchestrator.execute_pipeline(ctx)
        
    assert result == "FAILED"
    assert ctx.metadata.get("PROJECT_READY") == "NO"
