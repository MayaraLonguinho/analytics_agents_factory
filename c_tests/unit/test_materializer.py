import os
import pytest
from a_platform.g_materializer.materializer import Materializer
from a_platform.a_core.b_domain.artifact import Artifact

def test_materializer(tmp_path):
    base_dir = str(tmp_path / "e_generated_projects")
    materializer = Materializer(base_dir=base_dir)
    
    artifacts = [
        Artifact(name="main", path="src/main.py", content="print('hello')")
    ]
    
    project_dir = materializer.materialize("test-proj", artifacts)
    
    assert os.path.exists(project_dir)
    assert os.path.exists(os.path.join(project_dir, "src/main.py"))
    
    with open(os.path.join(project_dir, "src/main.py"), "r") as f:
        content = f.read()
        assert content == "print('hello')\n"
