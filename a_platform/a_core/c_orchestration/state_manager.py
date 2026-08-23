from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Any

class ProjectPhase(Enum):
    INIT = auto()
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
        
        self.phases: Dict[ProjectPhase, PhaseState] = {
            phase: PhaseState(name=phase.name) for phase in ProjectPhase
        }
        self.phases[ProjectPhase.INIT].status = PhaseStatus.COMPLETED

    def transition_to(self, new_phase: ProjectPhase):
        if self.current_phase != ProjectPhase.FAILED and self.current_phase != ProjectPhase.READY:
            self.phases[self.current_phase].status = PhaseStatus.COMPLETED
            
        self.current_phase = new_phase
        self.phases[new_phase].status = PhaseStatus.IN_PROGRESS
        print(f"[StateManager] Transição para a fase: {new_phase.name}")

    def fail_phase(self, phase: ProjectPhase, reason: str):
        self.phases[phase].status = PhaseStatus.FAILED
        self.phases[phase].details["error"] = reason
        self.current_phase = ProjectPhase.FAILED
        self.project_ready = False
        print(f"[StateManager] Falha na fase {phase.name}: {reason}")

    def complete_project(self):
        if self.current_phase != ProjectPhase.FAILED:
            self.current_phase = ProjectPhase.READY
            self.phases[ProjectPhase.READY].status = PhaseStatus.COMPLETED
            self.project_ready = True
            print("[StateManager] PROJETO PRONTO! (PROJECT READY = YES)")

    def get_status(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "current_phase": self.current_phase.name,
            "project_ready": self.project_ready,
            "repair_attempts": self.repair_attempts,
            "phases": {p.name: s.status.name for p, s in self.phases.items()}
        }
