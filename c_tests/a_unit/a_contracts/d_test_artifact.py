"""
c_tests/a_unit/a_contracts/d_test_artifact.py
==========================================
Especificação executável do contrato Artifact.
Valida identificação de artefatos, caminhos relativos, tipos e rejeição de campos extras.
"""
import pytest
from pydantic import ValidationError

from a_platform.b_contracts.g_artifact import Artifact


def test_artifact_valid_instantiation():
    """Valida a criação canônica de um Artifact."""
    art = Artifact(
        identity="art_001",
        name="model.py",
        path="src/model.py",
        type="code",
        content="class Model: pass",
        metadata={"language": "python"},
        producer="DataAgent",
    )
    assert art.identity == "art_001"
    assert art.name == "model.py"
    assert art.path == "src/model.py"
    assert art.type == "code"
    assert art.content == "class Model: pass"
    assert art.metadata == {"language": "python"}
    assert art.producer == "DataAgent"


def test_artifact_requires_mandatory_fields():
    """Valida que identity, name, path e type são campos obrigatórios."""
    with pytest.raises(ValidationError):
        Artifact(identity="art_incomplete")


def test_artifact_forbids_extra_fields():
    """Valida que campos não previstos no contrato são rejeitados."""
    with pytest.raises(ValidationError):
        Artifact(
            identity="art_002",
            name="test.py",
            path="tests/test.py",
            type="test",
            extra_payload="forbidden",
        )
