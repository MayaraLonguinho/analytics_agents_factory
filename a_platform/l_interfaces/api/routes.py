import uuid
import asyncio
from typing import Dict, Any
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator

router = APIRouter()

# Global memory for job tracking
jobs: Dict[str, Any] = {}

class SubmitRequest(BaseModel):
    prompt: str

class SubmitResponse(BaseModel):
    job_id: str
    status: str

async def background_run_pipeline(job_id: str, prompt: str):
    orchestrator = MasterOrchestrator()
    jobs[job_id] = orchestrator.state
    # Run the pipeline and it updates its own state object
    await orchestrator.run_pipeline(prompt)

@router.post("/project/submit", response_model=SubmitResponse)
async def submit_project(request: SubmitRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    # Pre-populate state
    jobs[job_id] = {"status": "INITIALIZED"}
    background_tasks.add_task(background_run_pipeline, job_id, request.prompt)
    return SubmitResponse(job_id=job_id, status="STARTED")

@router.get("/project/{job_id}/status")
def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    state = jobs[job_id]
    
    # If it's the state manager object from orchestrator
    if hasattr(state, "get"):
        status = state.get("status")
        project_plan = state.get("project_plan")
        plan_dict = project_plan.model_dump() if project_plan else None
        
        return {
            "job_id": job_id,
            "status": status,
            "plan": plan_dict
        }
    
    # If it's the raw dict before start
    return {
        "job_id": job_id,
        "status": state.get("status", "UNKNOWN"),
        "plan": None
    }

@router.get("/project/{job_id}/certificate")
def get_certificate(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    state = jobs[job_id]
    if hasattr(state, "get"):
        cert = state.get("certification")
        if cert:
            return cert.model_dump()
        return {"message": "Certification not ready"}
    
    return {"message": "Certification not ready"}
