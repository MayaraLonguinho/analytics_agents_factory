"""
c_tests/b_system/f_repair/b_test_responsible_phase.py
===================================================
Especificação executável de mapeamento da fase responsável (ResponsiblePhase).
Valida que falhas em runtime/gates são mapeadas para fases anteriores
(Architecture, Planner, Factory ou Ingestion) conforme a origem real da causa raiz.
"""
import pytest


def resolve_responsible_phase_for_failure(category: str) -> str:
    """Mapeamento determinístico de categoria de causa raiz para a fase responsável."""
    mapping = {
        "incompatible_stack": "ARCHITECTURE",
        "missing_task_dependency": "PLANNER",
        "wrong_agent_assignment": "PLANNER",
        "missing_artifact": "PROJECT_FACTORY",
        "corrupted_csv": "DATASET_PROFILING",
        "unclear_requirements": "DISCOVERY",
    }
    return mapping.get(category, "PROJECT_FACTORY")


def test_responsible_phase_mapping_across_lifecycle():
    """Valida o mapeamento transversal de causas raiz para fases específicas do ciclo de vida."""
    assert resolve_responsible_phase_for_failure("incompatible_stack") == "ARCHITECTURE"
    assert resolve_responsible_phase_for_failure("missing_task_dependency") == "PLANNER"
    assert resolve_responsible_phase_for_failure("missing_artifact") == "PROJECT_FACTORY"
    assert resolve_responsible_phase_for_failure("corrupted_csv") == "DATASET_PROFILING"
    assert resolve_responsible_phase_for_failure("unclear_requirements") == "DISCOVERY"
