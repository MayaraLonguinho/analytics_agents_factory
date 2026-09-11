import pytest
from a_platform.a_core.b_domain.project_plan import ProjectPlan, Task

def test_valid_dag():
    plan = ProjectPlan(project_id="p1", domain="analytics")
    
    plan.add_task(Task(id="t1", name="Ingest", description="", agent="data"))
    plan.add_task(Task(id="t2", name="Profile", description="", agent="data", dependencies=["t1"]))
    plan.add_task(Task(id="t3", name="ETL", description="", agent="data", dependencies=["t2"]))
    
    assert plan.validate_dag() is True
    assert plan.validated is True

def test_dag_with_missing_dependency():
    plan = ProjectPlan(project_id="p1", domain="analytics")
    
    plan.add_task(Task(id="t1", name="Ingest", description="", agent="data"))
    plan.add_task(Task(id="t2", name="Profile", description="", agent="data", dependencies=["t99"]))
    
    with pytest.raises(ValueError, match="depende da tarefa inexistente t99"):
        plan.validate_dag()

def test_dag_with_cycle():
    plan = ProjectPlan(project_id="p1", domain="analytics")
    
    plan.add_task(Task(id="t1", name="Ingest", description="", agent="data", dependencies=["t3"]))
    plan.add_task(Task(id="t2", name="Profile", description="", agent="data", dependencies=["t1"]))
    plan.add_task(Task(id="t3", name="ETL", description="", agent="data", dependencies=["t2"]))
    
    with pytest.raises(ValueError, match="ciclo de dependências"):
        plan.validate_dag()

def test_empty_plan_fails():
    plan = ProjectPlan(project_id="p1", domain="analytics")
    assert plan.validate_dag() is False
