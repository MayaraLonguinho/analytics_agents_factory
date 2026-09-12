import os
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.a_core.a_contracts.d_project_contract import ProjectPlan, Task
from a_platform.a_core.a_contracts.e_execution_contract import Artifact

from a_platform.h_factory.a_project_factory.a_project_factory import ProjectFactory
from a_platform.h_factory.d_artifact_materializer.a_materializer import ArtifactMaterializer
from a_platform.d_agents.m_agent_factory.a_agent_factory import AgentFactory
from a_platform.g_llm_gateway.e_gateway import LLMGateway
from a_platform.f_mcp.e_executor.a_executor import MCPExecutor
from a_platform.j_runtime.c_runtime import execute_project

class MockAgent:
    def execute_task(self, task: Task, req: ExecutionContext) -> list[Artifact]:
        return [Artifact(name=art_name, content=f"print('Executando {art_name}')\n", type="code") for art_name in task.expected_artifacts]

class MockAgentFactory(AgentFactory):
    def __init__(self):
        pass
    def get_agent(self, agent_name: str):
        return MockAgent()

def test_pipeline():
    print("--- 1. Preparando Contexto Sintético ---")
    req = ExecutionContext(prompt="Teste", project_id="demo-synth-001", domain="analytics")
    
    plan = ProjectPlan(
        project_id="demo-synth-001",
        domain="analytics",
        tasks=[
            Task(
                id="t1", 
                name="ETL Pipeline",
                description="Extract, Transform, Load",
                agent="TestingAgent", 
                skills=["python"], 
                dependencies=[],
                inputs=[],
                expected_artifacts=["etl/pipeline.py", "tests/test_pipeline.py"]
            )
        ],
        run_commands=["python3 etl/pipeline.py", "python3 tests/test_pipeline.py"]
    )
    req.project_plan = plan
    
    # Adicionar discovery_data mínimo para garantir o domain na pasta final
    req.discovery_data = {"domain": "analytics"}
    
    print("--- 2. Rodando ProjectFactory ---")
    # Mock LLMGateway bypass since we don't want LLM for requirements
    class MockGateway:
        async def generate(self, *args, **kwargs):
            class MockResp:
                content = "pytest"
            return MockResp()
    gateway = MockGateway()
    
    factory = ProjectFactory(MockAgentFactory(), gateway)
    artifacts = factory.assemble_project(req)
    for art in artifacts:
        print(f"Gerado: {art.name}")
        
    print("\n--- 3. Rodando Materializer ---")
    mcp = MCPExecutor()
    materializer = ArtifactMaterializer(mcp)
    success = materializer.materialize(req, artifacts)
    print(f"Materialização sucesso? {success}")
    
    print("\n--- 4. Rodando Runtime ---")
    project_path = os.path.join(os.getcwd(), "e_generated_projects", "analytics", "demo-synth-001")
    result = execute_project(req, project_path=project_path)
    
    print(f"Status: {result.status}")
    print(f"Exit Code: {result.exit_code}")
    print(f"Stdout:\n{result.stdout}")
    print(f"Stderr:\n{result.stderr}")
    print(f"Diagnosis:\n{result.diagnosis}")
    
    if result.status == "SUCCESS" and success:
        print("\n✅ PIPELINE VALIDADA COM SUCESSO!")
    else:
        print("\n❌ FALHA NA PIPELINE.")

if __name__ == "__main__":
    test_pipeline()
