# pyrefly: ignore [missing-import]
import pytest
from a_platform.l_certification.certification_engine import CertificationEngine
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.c_orchestration.state_manager import StateManager, ProjectPhase, PhaseStatus

def test_certification_fails_if_discovery_not_completed():
    engine = CertificationEngine()
    request = ProjectRequest(prompt="test", project_id="test_cert_1")
    request.metadata["quality_score"] = 95.0
    
    state_manager = StateManager(project_id="test_cert_1")
    # All phases completed EXCEPT discovery
    state_manager.phases[ProjectPhase.DISCOVERY].status = PhaseStatus.IN_PROGRESS
    state_manager.phases[ProjectPhase.PLANNER].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.MATERIALIZATION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.EXECUTION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.VALIDATION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.QUALITY].status = PhaseStatus.COMPLETED
    
    result = engine.run_certification(request, state_manager)
    
    assert result is False
    assert request.metadata.get("certification_tier") is None

def test_certification_fails_if_planner_not_completed():
    engine = CertificationEngine()
    request = ProjectRequest(prompt="test", project_id="test_cert_2")
    request.metadata["quality_score"] = 95.0
    
    state_manager = StateManager(project_id="test_cert_2")
    state_manager.phases[ProjectPhase.DISCOVERY].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.PLANNER].status = PhaseStatus.FAILED
    state_manager.phases[ProjectPhase.MATERIALIZATION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.EXECUTION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.VALIDATION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.QUALITY].status = PhaseStatus.COMPLETED
    
    result = engine.run_certification(request, state_manager)
    
    assert result is False

def test_certification_fails_if_materialization_not_completed():
    engine = CertificationEngine()
    request = ProjectRequest(prompt="test", project_id="test_cert_3")
    request.metadata["quality_score"] = 95.0
    
    state_manager = StateManager(project_id="test_cert_3")
    state_manager.phases[ProjectPhase.DISCOVERY].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.PLANNER].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.MATERIALIZATION].status = PhaseStatus.PENDING
    state_manager.phases[ProjectPhase.EXECUTION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.VALIDATION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.QUALITY].status = PhaseStatus.COMPLETED
    
    result = engine.run_certification(request, state_manager)
    
    assert result is False

def test_certification_passes_if_all_completed():
    engine = CertificationEngine()
    request = ProjectRequest(prompt="test", project_id="test_cert_4")
    request.metadata["quality_score"] = 95.0
    
    state_manager = StateManager(project_id="test_cert_4")
    state_manager.phases[ProjectPhase.DISCOVERY].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.PLANNER].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.MATERIALIZATION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.EXECUTION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.VALIDATION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.QUALITY].status = PhaseStatus.COMPLETED
    
    result = engine.run_certification(request, state_manager)
    
    assert result is True
    assert request.metadata.get("certification_tier") == "PLATINUM"
