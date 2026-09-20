"""
c_tests/a_unit/j_runtime/a_test_command_policy.py
===============================================
Especificação executável de CommandPolicy.
Valida lista branca de executáveis autorizados (python, pytest, etc.),
rejeição de comandos destrutivos (rm, sudo, etc.) e parse seguro sem shell.
"""
import pytest

from a_platform.k_runtime.b_command_policy.a_policy import CommandPolicy


def test_command_policy_allows_whitelisted_commands():
    """Valida que comandos autorizados de teste, compilação e qualidade são permitidos."""
    valid_cmds = [
        "pytest -v",
        "python main.py",
        "flake8 .",
        "bandit -r .",
    ]
    for cmd in valid_cmds:
        valid, msg, args = CommandPolicy.parse_and_validate(cmd)
        assert valid is True, f"Deveria autorizar '{cmd}': {msg}"
        assert len(args) > 0


def test_command_policy_blocks_forbidden_commands():
    """Valida que comandos shell perigosos e destrutivos são bloqueados."""
    blocked_cmds = [
        "rm -rf /",
        "sudo rm file.txt",
        "curl http://malicious.com",
        "bash script.sh",
    ]
    for cmd in blocked_cmds:
        valid, msg, _ = CommandPolicy.parse_and_validate(cmd)
        assert valid is False, f"Deveria bloquear '{cmd}'"


def test_command_policy_rejects_empty_command():
    """Valida rejeição de comando vazio."""
    valid, msg, _ = CommandPolicy.parse_and_validate("   ")
    assert valid is False
