import os
from unittest.mock import Mock

from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.a_core.a_contracts.d_project_contract import ProjectPlan, Task
from a_platform.a_core.d_session.c_state import StateManager, ProjectPhase, PhaseStatus
from a_platform.j_runtime.c_runtime import ExecutionResult

from a_platform.k_validation.a_validation_gate import ValidationGate
from a_platform.l_quality.a_quality_engine import QualityEngine
from a_platform.m_certification.a_certification_engine import CertificationEngine
from a_platform.n_orchestration.c_repair_loop import RepairLoop
from a_platform.a_core.a_contracts.f_gate_contract import ReadinessResult

def create_context():
    req = ExecutionContext(prompt="Teste Gates", project_id="demo-gates-001", domain="analytics")
    plan = ProjectPlan(
        project_id="demo-gates-001",
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
                expected_artifacts=["etl/pipeline.py", "requirements.txt"]
            )
        ],
        run_commands=["python3 etl/pipeline.py"]
    )
    req.project_plan = plan
    req.discovery_data = {"domain": "analytics"}
    
    # Mocking files
    project_dir = os.path.join(os.getcwd(), "e_generated_projects", "analytics", "demo-gates-001")
    os.makedirs(os.path.join(project_dir, "etl"), exist_ok=True)
    
    with open(os.path.join(project_dir, "etl", "pipeline.py"), "w") as f:
        f.write("print('ETL executado com sucesso')\n")
        
    with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
        f.write("pytest\n")
        
    return req, project_dir


def test_success_scenario():
    print("\n=== CENÁRIO 1: SUCESSO TOTAL ===")
    req, _ = create_context()
    
    exec_result = ExecutionResult(status="SUCCESS", exit_code=0, stdout="OK", diagnosis="Execução concluída com sucesso.")
    
    val_gate = ValidationGate()
    val_report = val_gate.evaluate(req, exec_result)
    print(f"Validation: {val_report.status}")
    for c in val_report.checks:
        print(f"  - {c.name}: {c.status} ({c.details})")
    
    qual_eng = QualityEngine()
    qual_report = qual_eng.evaluate(req, validation_result={"passed": val_report.passed}, runtime_result=exec_result.to_dict())
    print(f"Quality: {qual_report.overall_status} (Score: {qual_report.score})")
    
    cert_eng = CertificationEngine()
    cert_result = cert_eng.evaluate(req, execution_result=exec_result.to_dict(), validation_result={"passed": val_report.passed}, quality_result=qual_report.to_dict())
    print(f"Certification: {cert_result.status} (Score: {cert_result.score})")
    
    # StateManager setup
    sm = StateManager("demo-gates-001")
    sm.phases[ProjectPhase.DISCOVERY].status = PhaseStatus.COMPLETED
    sm.phases[ProjectPhase.PLANNER].status = PhaseStatus.COMPLETED
    sm.phases[ProjectPhase.MATERIALIZATION].status = PhaseStatus.COMPLETED
    
    is_ready = ReadinessGate.evaluate(
        sm, 
        execution_result=exec_result,
        validation_result=val_report,
        quality_result=qual_report,
        certification_result=cert_result
    )
    print(f"Project Ready: {is_ready}")
    assert is_ready is True
    

def test_failure_scenario():
    print("\n=== CENÁRIO 2: FALHA NA EXECUÇÃO ACIONANDO REPAIR ===")
    req, _ = create_context()
    
    exec_result = ExecutionResult(status="FAILED", exit_code=1, stdout="", stderr="ImportError: missing module", diagnosis="Erro de execução em: python3 etl/pipeline.py")
    
    val_gate = ValidationGate()
    val_report = val_gate.evaluate(req, exec_result)
    print(f"Validation: {val_report.status}")
    
    qual_eng = QualityEngine()
    qual_report = qual_eng.evaluate(req, validation_result={"passed": val_report.passed}, runtime_result=exec_result.to_dict())
    print(f"Quality: {qual_report.overall_status} (Score: {qual_report.score})")
    
    cert_eng = CertificationEngine()
    cert_result = cert_eng.evaluate(req, execution_result=exec_result.to_dict(), validation_result={"passed": val_report.passed}, quality_result=qual_report.to_dict())
    print(f"Certification: {cert_result.status} (Score: {cert_result.score})")
    
    # StateManager setup
    sm = StateManager("demo-gates-001")
    sm.phases[ProjectPhase.DISCOVERY].status = PhaseStatus.COMPLETED
    sm.phases[ProjectPhase.PLANNER].status = PhaseStatus.COMPLETED
    sm.phases[ProjectPhase.MATERIALIZATION].status = PhaseStatus.COMPLETED
    
    is_ready = ReadinessGate.evaluate(
        sm, 
        execution_result=exec_result,
        validation_result=val_report,
        quality_result=qual_report,
        certification_result=cert_result
    )
    print(f"Project Ready: {is_ready}")
    assert is_ready is False
    
    print("\n-> Acionando Repair Loop simulado...")
    class MockAgentFactory:
        def get_agent(self, agent_name):
            class M:
                name = agent_name
            return M()
            
    class MockLearning:
        def log_correction(self, *args, **kwargs):
            print("Correction logged.")
            
    # Mock gateway
    class MockGateway:
        async def generate(self, *args, **kwargs):
            class MockResp:
                content = '```json\n{"file_name": "etl/pipeline.py", "agent_type": "DataAgent", "fixed_content": "print(\'FIXED ETL\')\\n"}\n```'
            return MockResp()
            
    # Instancia o repair_loop, mas monkey patch no gateway logo após instanciar? Não, LLMGateway falha no __init__.
    # Vamos mockar a classe LLMGateway no módulo? Ou simplesmente mockar o a_repair_loop.LLMGateway.
    import a_platform.n_orchestration.c_repair_loop as rl
    rl.LLMGateway = MockGateway
    
    repair_loop = RepairLoop(MockAgentFactory(), MockLearning())
    
    success = repair_loop.run_repair(req, exec_result)
    print(f"Repair Sucesso: {success}")
    assert success is True

if __name__ == "__main__":
    test_success_scenario()
    test_failure_scenario()
