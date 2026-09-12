import sys
import os

# Add root to pythonpath
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from a_platform.a_core.d_session.b_context import ExecutionContext, Decision
from a_platform.a_core.a_contracts.d_project_contract import ProjectPlan, ProjectTask
from a_platform.c_brain.h_brain import Brain
from a_platform.c_brain.f_graph.b_graph_builder import GraphBuilder

def test_graph_builder():
    brain = Brain()
    
    # Mocking Context
    context = ExecutionContext()
    context.project_id = "test_sales_001"
    context.project_type = "Sales Analytics"
    context.domain = "sales"
    context.dataset_profile = {"file_name": "data.csv"}
    
    task1 = ProjectTask(
        task_id="t1",
        name="Profile Data",
        assigned_agent="DataAgent",
        required_skills=["profile_dataset"],
    )
    task2 = ProjectTask(
        task_id="t2",
        name="Generate SQL",
        assigned_agent="DatabaseAgent",
        required_skills=["sql_generation"],
    )
    task3 = ProjectTask(
        task_id="t3",
        name="Analyze",
        assigned_agent="AnalyticsAgent",
        required_skills=["analytics", "Validation", "Quality", "Certification"]
    )
    context.project_plan = ProjectPlan(project_id="test_sales_001", tasks=[task1, task2, task3])
    
    builder = GraphBuilder(brain=brain)
    builder.build_graph(context)
    
    print("Grafo construído e exportado com sucesso.")

if __name__ == "__main__":
    test_graph_builder()
