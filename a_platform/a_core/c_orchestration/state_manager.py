import os
import json
import logging
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.project_plan import ProjectPlan, Task

logger = logging.getLogger(__name__)

class ProjectPhase(Enum):
    INIT = auto()
    NEEDS_INPUT = auto()
    DISCOVERY = auto()
    DATASET_PROFILING = auto()
    BRAIN = auto()
    ARCHITECTURE = auto()
    PLANNER = auto()
    PROJECT_FACTORY = auto()
    MATERIALIZATION = auto()
    EXECUTION = auto()
    VALIDATION = auto()
    REPAIR_LOOP = auto()
    QUALITY = auto()
    CERTIFICATION = auto()
    READY = auto()
    FAILED = auto()

class PhaseStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    PAUSED = auto()
    COMPLETED = auto()
    FAILED = auto()

@dataclass
class PhaseState:
    name: str
    status: PhaseStatus = PhaseStatus.PENDING
    details: Dict[str, Any] = field(default_factory=dict)

class StateManager:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.current_phase: ProjectPhase = ProjectPhase.INIT
        self.project_ready: bool = False
        self.repair_attempts: int = 0
        self.max_repair_attempts: int = 3
        self.state_dir = os.path.join(os.getcwd(), ".aaf_state")
        
        self.phases: Dict[ProjectPhase, PhaseState] = {
            phase: PhaseState(name=phase.name) for phase in ProjectPhase
        }
        self.phases[ProjectPhase.INIT].status = PhaseStatus.COMPLETED

        if not os.path.exists(self.state_dir):
            os.makedirs(self.state_dir)

    def transition_to(self, new_phase: ProjectPhase):
        if self.current_phase not in [ProjectPhase.FAILED, ProjectPhase.READY, ProjectPhase.NEEDS_INPUT]:
            self.phases[self.current_phase].status = PhaseStatus.COMPLETED
            
        self.current_phase = new_phase
        self.phases[new_phase].status = PhaseStatus.IN_PROGRESS
        logger.info(f"[StateManager] Transição para a fase: {new_phase.name}")

    def pause_for_input(self):
        if self.current_phase != ProjectPhase.FAILED and self.current_phase != ProjectPhase.READY:
            self.phases[self.current_phase].status = PhaseStatus.PAUSED
        self.current_phase = ProjectPhase.NEEDS_INPUT
        self.phases[ProjectPhase.NEEDS_INPUT].status = PhaseStatus.IN_PROGRESS
        logger.info("[StateManager] Pipeline pausado aguardando input do usuário.")

    def fail_phase(self, phase: ProjectPhase, reason: str):
        self.phases[phase].status = PhaseStatus.FAILED
        self.phases[phase].details["error"] = reason
        self.current_phase = ProjectPhase.FAILED
        self.project_ready = False
        logger.error(f"[StateManager] Falha na fase {phase.name}: {reason}")

    def complete_project(self):
        if self.current_phase != ProjectPhase.FAILED:
            self.current_phase = ProjectPhase.READY
            self.phases[ProjectPhase.READY].status = PhaseStatus.COMPLETED
            self.project_ready = True
            logger.info("[StateManager] PROJETO PRONTO! (PROJECT READY = YES)")

    def get_status(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "current_phase": self.current_phase.name,
            "project_ready": self.project_ready,
            "repair_attempts": self.repair_attempts,
            "phases": {p.name: s.status.name for p, s in self.phases.items()}
        }

    def save_state(self, request: ProjectRequest):
        state_file = os.path.join(self.state_dir, f"{self.project_id}.json")
        
        # Serialize request carefully (ProjectPlan is custom)
        req_dict = {
            "prompt": request.prompt,
            "dataset_path": request.dataset_path,
            "domain": request.domain,
            "project_id": request.project_id,
            "metadata": request.metadata,
            "discovery_data": request.discovery_data,
            "dataset_profile": request.dataset_profile,
            "architecture_decision": request.architecture_decision,
            "graph_representation": request.graph_representation,
            "artifacts": request.artifacts,
            "project_plan": None
        }
        
        if request.project_plan:
            req_dict["project_plan"] = {
                "tasks": [asdict(t) for t in request.project_plan.tasks],
                "run_commands": request.project_plan.run_commands
            }
            
        data = {
            "state_manager": {
                "current_phase": self.current_phase.name,
                "project_ready": self.project_ready,
                "repair_attempts": self.repair_attempts,
                "phases": {p.name: {"status": s.status.name, "details": s.details} for p, s in self.phases.items()}
            },
            "request": req_dict
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"[StateManager] Estado salvo em {state_file}")

    @classmethod
    def load_state(cls, project_id: str) -> tuple['StateManager', ProjectRequest]:
        state_dir = os.path.join(os.getcwd(), ".aaf_state")
        state_file = os.path.join(state_dir, f"{project_id}.json")
        
        if not os.path.exists(state_file):
            raise FileNotFoundError(f"Estado do projeto {project_id} não encontrado.")
            
        with open(state_file, 'r') as f:
            data = json.load(f)
            
        sm_data = data["state_manager"]
        sm = cls(project_id)
        sm.current_phase = ProjectPhase[sm_data["current_phase"]]
        sm.project_ready = sm_data["project_ready"]
        sm.repair_attempts = sm_data["repair_attempts"]
        
        for p_name, p_state in sm_data["phases"].items():
            phase_enum = ProjectPhase[p_name]
            sm.phases[phase_enum].status = PhaseStatus[p_state["status"]]
            sm.phases[phase_enum].details = p_state["details"]
            
        req_data = data["request"]
        plan = None
        if req_data.get("project_plan"):
            tasks = [Task(**t) for t in req_data["project_plan"]["tasks"]]
            plan = ProjectPlan(
                project_id=project_id,
                domain=req_data.get("domain", ""),
                tasks=tasks,
                run_commands=req_data["project_plan"].get("run_commands", [])
            )
            
        request = ProjectRequest(
            prompt=req_data["prompt"],
            dataset_path=req_data.get("dataset_path"),
            domain=req_data.get("domain"),
            project_id=project_id,
            metadata=req_data.get("metadata", {}),
            discovery_data=req_data.get("discovery_data", {}),
            dataset_profile=req_data.get("dataset_profile", {}),
            architecture_decision=req_data.get("architecture_decision", {}),
            graph_representation=req_data.get("graph_representation", {}),
            artifacts=req_data.get("artifacts", []),
            project_plan=plan
        )
        
        return sm, request
