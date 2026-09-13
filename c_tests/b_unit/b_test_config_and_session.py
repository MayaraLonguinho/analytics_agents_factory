import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.a_core.d_session.a_session import AAFSession
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.a_core.d_session.c_state import StateManager

def test_session_initialization():
    session = AAFSession(session_id="test_sess")
    assert session.session_id == "test_sess"
    assert isinstance(session.context, ExecutionContext)
    assert isinstance(session.state_manager, StateManager)
    
def test_state_manager_transitions():
    sm = StateManager(project_id="test_proj")
    from a_platform.a_core.d_session.c_state import ProjectPhase, PhaseStatus
    assert sm.current_phase == ProjectPhase.INIT
    sm.transition_to(ProjectPhase.DISCOVERY)
    assert sm.current_phase == ProjectPhase.DISCOVERY
    assert sm.phases[ProjectPhase.DISCOVERY].status == PhaseStatus.IN_PROGRESS
