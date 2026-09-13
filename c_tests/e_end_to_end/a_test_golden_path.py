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

@patch("a_platform.f_mcp.e_executor.a_executor.MCPExecutor.execute")
@patch("a_platform.g_llm_gateway.e_gateway.LLMGateway.structured_output")
@patch("a_platform.g_llm_gateway.e_gateway.LLMGateway.generate")
@patch("a_platform.d_agents.c_planner.k_planner_agent.PlannerAgent.generate_plan")
def test_golden_path(mock_planner, mock_generate, mock_structured, mock_mcp):
    mock_generate.return_value = LLMResponse(content='{"domain": "mock_domain", "patterns": []}', model="mock", provider="mock")
    mock_structured.return_value = LLMResponse(content='{"architecture": "mock"}', model="mock", provider="mock")
    mock_mcp.return_value = {"status": "ok"}
    
    # Mock planner to return a simple valid plan so it bypasses LLM
    def side_effect_plan(request):
        request.project_plan = ProjectPlan(
            project_id=request.project_id,
            tasks=[ProjectTask(task_id="t1", name="Create app", assigned_agent="DataAgent")]
        )
        return True
        
    mock_planner.side_effect = side_effect_plan

    orchestrator = MasterOrchestrator()
    
    # Prepara mock runtime success
    # Para passar pelo Readiness, ele verifica a exec, val, qual, cert com base em discos
    # Como e_generated_projects/test_proj_golden não tem nada, QualityEngine reprovaria tests e code
    # Vamos injetar artefatos reais temporarios.
    
    proj_id = "test_proj_golden"
    test_path = f"e_generated_projects/{proj_id}"
    os.makedirs(test_path, exist_ok=True)
    with open(f"{test_path}/main.py", "w") as f:
        f.write("print('hello')")
    with open(f"{test_path}/test_main.py", "w") as f:
        f.write("def test_dummy(): pass")
    with open(f"{test_path}/requirements.txt", "w") as f:
        f.write("pytest")
    with open(f"{test_path}/README.md", "w") as f:
        f.write("# doc")
        
    ctx = ExecutionContext(
        project_id=proj_id, 
        prompt="Create basic app", 
        domain="analytics",
        discovery_data={"domain": "analytics"}
    )
    
    # Mock execution result to bypass real runtime 
    from a_platform.a_core.a_contracts.e_execution_contract import ExecutionResult
    orchestrator.last_execution_result = ExecutionResult(task_id="t1", success=True)
    
    # Patches para simular sucesso no Execution step
    with patch("a_platform.j_runtime.a_execution.c_runtime.ProjectRuntime.execute", return_value=ExecutionResult(task_id="t1", success=True)):
        result = orchestrator.execute_pipeline(ctx)
    
    # Limpa
    shutil.rmtree(test_path)
    
    assert result == "SUCCESS"
    assert ctx.metadata.get("PROJECT_READY") == "YES"
