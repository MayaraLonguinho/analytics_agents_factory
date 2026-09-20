"""
c_tests/b_system/a_planning/d_test_execution_plan.py
==================================================
Especificação executável de planos de execução em DAG (Directed Acyclic Graph).
Valida topologia linear, topologia ramificada e detecção de ciclos como erro estrito.
"""
from collections import defaultdict, deque
import pytest

from a_platform.b_contracts.e_task import ProjectTask


def topological_sort(tasks):
    """Função de ordenação topológica de referência para validação da DAG."""
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    task_map = {t.task_id: t for t in tasks}

    for t in tasks:
        in_degree[t.task_id] = 0

    for t in tasks:
        for dep in t.dependencies:
            graph[dep].append(t.task_id)
            in_degree[t.task_id] += 1

    queue = deque([tid for tid in in_degree if in_degree[tid] == 0])
    ordered = []

    while queue:
        curr = queue.popleft()
        ordered.append(task_map[curr])
        for neighbor in graph[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(ordered) != len(tasks):
        raise ValueError("Ciclo detectado na DAG de execução.")

    return ordered


def test_linear_dag_execution_plan():
    """Valida a ordenação de DAG linear: Task A -> Task B -> Task C."""
    ta = ProjectTask(task_id="A", name="Task A", dependencies=[])
    tb = ProjectTask(task_id="B", name="Task B", dependencies=["A"])
    tc = ProjectTask(task_id="C", name="Task C", dependencies=["B"])

    ordered = topological_sort([tc, ta, tb])
    assert [t.task_id for t in ordered] == ["A", "B", "C"]


def test_branched_dag_execution_plan():
    """Valida a ordenação de DAG ramificada: A -> (B, C) -> D."""
    ta = ProjectTask(task_id="A", name="Task A", dependencies=[])
    tb = ProjectTask(task_id="B", name="Task B", dependencies=["A"])
    tc = ProjectTask(task_id="C", name="Task C", dependencies=["A"])
    td = ProjectTask(task_id="D", name="Task D", dependencies=["B", "C"])

    ordered = topological_sort([td, tc, tb, ta])
    order_ids = [t.task_id for t in ordered]
    assert order_ids[0] == "A"
    assert set(order_ids[1:3]) == {"B", "C"}
    assert order_ids[3] == "D"


def test_cyclic_dag_raises_error():
    """Valida que dependências circulares A -> B -> C -> A levantam erro estrito."""
    ta = ProjectTask(task_id="A", name="Task A", dependencies=["C"])
    tb = ProjectTask(task_id="B", name="Task B", dependencies=["A"])
    tc = ProjectTask(task_id="C", name="Task C", dependencies=["B"])

    with pytest.raises(ValueError, match="Ciclo detectado"):
        topological_sort([ta, tb, tc])
