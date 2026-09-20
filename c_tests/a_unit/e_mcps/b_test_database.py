"""
c_tests/a_unit/e_mcps/b_test_database.py
======================================
Especificação executável de DatabaseMCP.
Valida execução de queries analíticas locais e bloqueio de comandos perigosos (ATTACH/DETACH).
"""
from pathlib import Path
import pytest

from a_platform.f_mcps.b_database.a_database_mcp import handle_database, is_safe_query


def test_database_mcp_select_query(tmp_path: Path):
    """Valida a execução de queries SELECT em banco SQLite local temporário."""
    db_file = tmp_path / "test.db"
    # Setup
    handle_database(
        "CREATE TABLE sales (id INT, amount FLOAT); INSERT INTO sales VALUES (1, 100.0);",
        db_path=str(db_file),
    )
    res = handle_database("SELECT * FROM sales;", db_path=str(db_file))
    assert res["success"] is True
    assert res["data"] == [(1, 100.0)]


def test_database_mcp_blocks_forbidden_attach():
    """Valida que comandos de anexo de bancos externos são bloqueados por segurança."""
    assert is_safe_query("ATTACH DATABASE '/etc/shadow' AS shadow;") is False

    res = handle_database("ATTACH DATABASE '/etc/shadow' AS shadow;")
    assert res["success"] is False
    assert "proibidas" in res["error"]
