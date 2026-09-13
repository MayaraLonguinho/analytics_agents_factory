import os
import pytest

@pytest.fixture(autouse=True)
def set_env_vars():
    os.environ["OPENAI_API_KEY"] = "sk-dummy"
    os.environ["GEMINI_API_KEY"] = "dummy"
    os.environ["ANTHROPIC_API_KEY"] = "dummy"
    yield
