"""
c_tests/a_unit/d_skills/d_test_dataset_profiling.py
=================================================
Especificação executável de DatasetProfilingSkill.
Valida análise estrutural de datasets, detecção de colunas, tipos, contagem de nulos,
tratamento de erros e imutabilidade dos dados brutos.
"""
from pathlib import Path
import pytest

from a_platform.e_skills.a_dataset_profiling.c_profiling.a_profiler import DatasetProfilingSkill


def test_profiling_valid_csv(tmp_path: Path):
    """Valida o profiling de um arquivo CSV sintético com tipos e nulos."""
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(
        "id,produto,valor,categoria\n"
        "1,Notebook,3500.0,Eletronicos\n"
        "2,Cadeira,,Moveis\n"
        "3,Monitor,900.0,Eletronicos\n"
    )

    skill = DatasetProfilingSkill()
    res = skill.execute({"dataset_path": str(csv_file)})
    assert "dataset_profile" in res
    profile = res["dataset_profile"]
    assert profile["row_count"] == 3
    assert profile["column_count"] == 4

    # Valida coluna com valor nulo
    valor_col = next(c for c in profile["columns"] if c["name"] == "valor")
    assert valor_col["null_count"] == 1
    assert valor_col["null_percentage"] == round(1 / 3 * 100, 2)


def test_profiling_missing_file_raises_error():
    """Valida que caminho inexistente levanta erro sem crash silencioso."""
    skill = DatasetProfilingSkill()
    with pytest.raises((RuntimeError, FileNotFoundError, ValueError)):
        skill.execute({"dataset_path": "/tmp/non_existent_dataset_123.csv"})


def test_profiling_does_not_mutate_dataset(tmp_path: Path):
    """Garante que a skill de profiling opera em modo estritamente read-only."""
    csv_file = tmp_path / "immutable.csv"
    original_content = "a,b\n1,2\n3,4\n"
    csv_file.write_text(original_content)

    skill = DatasetProfilingSkill()
    skill.execute({"dataset_path": str(csv_file)})

    # O conteúdo físico deve permanecer rigorosamente idêntico
    assert csv_file.read_text() == original_content
