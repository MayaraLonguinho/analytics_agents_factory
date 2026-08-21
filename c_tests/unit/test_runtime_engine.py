from unittest.mock import patch
from a_platform.h_runtime.runtime_engine import RuntimeEngine

@patch("a_platform.h_runtime.docker_controller.subprocess.run")
@patch("a_platform.h_runtime.health_checker.urllib.request.urlopen")
def test_runtime_engine(mock_urlopen, mock_run):
    class MockResponse:
        def getcode(self): return 200
    
    mock_run.return_value.returncode = 0
    mock_urlopen.return_value = MockResponse()
    
    engine = RuntimeEngine()
    result = engine.run_project("/dummy/dir")
    
    assert result is True
    mock_run.assert_called_once()
