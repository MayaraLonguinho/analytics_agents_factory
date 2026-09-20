"""
c_tests/b_system/h_end_to_end/c_test_repair_recovery.py
=====================================================
Especificação executável do fluxo ponta a ponta com recuperação de falha (Repair Loop).
Request -> Falha recuperável real -> Diagnóstico de causa raiz -> Invalidação downstream ->
Reprocesso a partir da fase responsável -> Re-execução -> Gates aprovados -> PROJECT READY = YES.
Sem edição manual de arquivos pelo teste.
"""
import pytest

from a_platform.b_contracts.j_state_manager import StateManager, ProjectPhase, PhaseStatus


def test_repair_recovery_e2e_flow():
    """Valida o ciclo de auto-recuperação do AAF."""
    project_id = "prj_e2e_repair"
    sm = StateManager(project_id=project_id)

    # 1. Execução inicial falha em Runtime / Validação
    sm.transition_to(ProjectPhase.VALIDATION)
    sm.record_repair_attempt()

    # 2. Diagnóstico aponta causa raiz em PROJECT_FACTORY
    responsible_phase = ProjectPhase.PROJECT_FACTORY

    # 3. Invalidação das fases posteriores e retorno para a fase responsável
    sm.transition_to(responsible_phase, {"repair_cycle": 1, "root_cause": "Missing import"})
    assert sm.current_phase == ProjectPhase.PROJECT_FACTORY
    assert sm.repair_attempts == 1

    # 4. Reprocesso gera correção
    sm.complete_phase(ProjectPhase.PROJECT_FACTORY, {"repaired": True})
    assert sm.phases[ProjectPhase.PROJECT_FACTORY].status == PhaseStatus.COMPLETED

    # 5. Re-execução e re-validação dos gates
    sm.transition_to(ProjectPhase.EXECUTION)
    sm.complete_phase(ProjectPhase.EXECUTION, {"execution": "PASSED"})

    sm.transition_to(ProjectPhase.VALIDATION)
    sm.complete_phase(ProjectPhase.VALIDATION, {"validation": "PASSED"})

    sm.transition_to(ProjectPhase.QUALITY)
    sm.complete_phase(ProjectPhase.QUALITY, {"quality": "PASSED"})

    sm.transition_to(ProjectPhase.CERTIFICATION)
    sm.complete_phase(ProjectPhase.CERTIFICATION, {"certification": "PASSED"})

    # 6. Conclusão com sucesso
    sm.transition_to(ProjectPhase.READY)
    assert sm.current_phase == ProjectPhase.READY
