from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

from .f_project_plan import ProjectPlan

@dataclass
class Decision:
    id: str  # Format: D-NN, Q-NN, QA-NN
    status: str  # e.g., 'adopted', 'pending_user', 'resolved'
    decision: str
    reason: str
    evidence: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class SkillRecord:
    skill_id: str
    status: str  # e.g., 'selected', 'executed', 'failed'
    artifacts_produced: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class Gates:
    discovery: str = "pending"
    planning: str = "pending"
    materialization: str = "pending"
    execution: str = "pending"
    validation: str = "pending"
    quality: str = "pending"
    certification: str = "pending"

@dataclass
class ExecutionContext:
    project_id: str = "proj_default"
    prompt: str = ""
    
    # Context
    project_type: Optional[str] = None
    business_context: Optional[str] = None
    domain: Optional[str] = None
    dataset_profile: Dict[str, Any] = field(default_factory=dict)
    architecture_decision: Dict[str, Any] = field(default_factory=dict)
    
    # Knowledge
    brain_context: Dict[str, Any] = field(default_factory=dict)
    
    # Decisions & Tracking
    decisions: List[Decision] = field(default_factory=list)
    skills: List[SkillRecord] = field(default_factory=list)
    gates: Gates = field(default_factory=Gates)
    
    # Plan
    project_plan: Optional[ProjectPlan] = None
    
    # Assumptions (during Discovery)
    assumptions: List[str] = field(default_factory=list)

    def add_decision(self, decision: Decision):
        self.decisions.append(decision)
        
    def add_assumption(self, assumption: str):
        self.assumptions.append(assumption)

    def freeze_context(self):
        """Freezes the context after discovery to avoid further architecture changes."""
        self.gates.discovery = "completed"
