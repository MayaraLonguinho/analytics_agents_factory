import pytest
from a_platform.h_runtime.runtime_engine import RuntimeEngine
import os

def test_runtime_engine(tmp_path):
    engine = RuntimeEngine()
    
    # Test valid directory
    valid_dir = tmp_path / "valid_project"
    valid_dir.mkdir()
    result = engine.run_project(str(valid_dir))
    assert result is True
    
    # Test invalid directory
    result_invalid = engine.run_project("/dummy/invalid/dir")
    assert result_invalid is False

