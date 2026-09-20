"""
c_tests/a_unit/e_mcps/c_test_docker.py
====================================
Especificação executável de DockerMCP.
Valida lista restrita de subcomandos autorizados e prevenção de shell injection.
"""
import pytest

from a_platform.f_mcps.c_docker.a_docker_mcp import handle_docker


def test_docker_mcp_rejects_disallowed_subcommands():
    """Valida que subcomandos de risco (ex: rm, system prune) são bloqueados."""
    res = handle_docker("system prune -a")
    assert res["success"] is False
    assert "não permitido" in res["error"]


def test_docker_mcp_rejects_empty_command():
    """Valida o tratamento de comandos vazios."""
    res = handle_docker("")
    assert res["success"] is False
    assert "Comando vazio" in res["error"]
