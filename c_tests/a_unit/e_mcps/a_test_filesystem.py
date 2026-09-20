"""
c_tests/a_unit/e_mcps/a_test_filesystem.py
========================================
Especificação executável do FilesystemMCP e PathPolicy.
Valida isolamento de sandbox, escrita e leitura em paths permitidos, e rejeição estrita
de path traversal e acessos fora de e_generated_projects.
"""
from pathlib import Path
import pytest

from a_platform.f_mcps.a_filesystem.a_filesystem_mcp import (
    handle_filesystem,
    is_safe_path,
    ALLOWED_ROOT,
)


def test_filesystem_mcp_path_within_sandbox(tmp_path: Path):
    """Valida que operações dentro do sandbox permitido são autorizadas."""
    target_file = Path(ALLOWED_ROOT) / "test_sandbox_proj" / "main.py"
    res = handle_filesystem(action="write", path=str(target_file), content="# valid code")
    assert res["success"] is True

    read_res = handle_filesystem(action="read", path=str(target_file))
    assert read_res["success"] is True
    assert read_res["content"] == "# valid code"

    # Limpeza
    if target_file.exists():
        target_file.unlink()
        target_file.parent.rmdir()


def test_filesystem_mcp_rejects_path_traversal():
    """Valida que tentativas de path traversal (ex: ../../etc/passwd) são bloqueadas."""
    malicious_path = f"{ALLOWED_ROOT}/../../etc/passwd"
    assert is_safe_path(malicious_path) is False

    res = handle_filesystem(action="write", path=malicious_path, content="hacked")
    assert res["success"] is False
    assert "Access denied" in res["error"]


def test_filesystem_mcp_rejects_arbitrary_absolute_path():
    """Valida que caminhos absolutos fora do boundary são estritamente negados."""
    arbitrary_path = "/tmp/outside_sandbox.py"
    assert is_safe_path(arbitrary_path) is False

    res = handle_filesystem(action="read", path=arbitrary_path)
    assert res["success"] is False
    assert "Access denied" in res["error"]
