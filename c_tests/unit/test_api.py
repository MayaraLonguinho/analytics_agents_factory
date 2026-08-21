import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the FastAPI app
from a_platform.l_interfaces.api.main_api import app
# Import jobs memory dict
from a_platform.l_interfaces.api.routes import jobs

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Analytics AI Factory API is running"}

@patch("a_platform.l_interfaces.api.routes.BackgroundTasks.add_task")
def test_submit_project(mock_bg_task):
    response = client.post(
        "/api/v1/project/submit",
        json={"prompt": "Test project"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "STARTED"
    
    # Verify it was added to memory
    job_id = data["job_id"]
    assert job_id in jobs
    assert jobs[job_id]["status"] == "INITIALIZED"
    
    # Verify background task was called
    assert mock_bg_task.called

def test_get_status_not_found():
    response = client.get("/api/v1/project/invalid_id/status")
    assert response.status_code == 404

def test_get_certificate_not_found():
    response = client.get("/api/v1/project/invalid_id/certificate")
    assert response.status_code == 404
