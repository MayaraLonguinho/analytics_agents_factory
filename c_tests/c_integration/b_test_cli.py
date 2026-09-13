import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

import subprocess
import sys

def test_cli_help():
    result = subprocess.run([sys.executable, "-m", "a_platform.b_interfaces.b_cli.c_commands", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Usage" in result.stdout or "usage" in result.stdout or result.stdout == ""
