import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.b_contracts import ProjectRequest, ProjectPlan, ProjectTask

def test_project_contract_instantiation():
    req = ProjectRequest(project_id="p1", prompt="test")
    assert req.project_id == "p1"
    
    task = ProjectTask(task_id="t1", name="Task 1", required_skills=["skill1"])
    assert task.task_id == "t1"
    
    plan = ProjectPlan(project_id="p1", tasks=[task])
    assert len(plan.tasks) == 1
