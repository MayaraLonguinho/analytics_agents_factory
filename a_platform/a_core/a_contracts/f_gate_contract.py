from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class GateContract(BaseModel):
    gate_id: str
    name: str
    description: str

class ValidationCheck(BaseModel):
    check_id: str
    passed: bool = False
    message: str = ""

class ValidationReport(BaseModel):
    status: str = "NOT_EXECUTED"
    passed: bool = False
    checks: List[ValidationCheck] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class QualityMetric(BaseModel):
    metric_id: str
    value: float = 0.0
    passed: bool = False

class QualityReport(BaseModel):
    overall_status: str = "NOT_EXECUTED"
    score: float = 0.0
    passed: bool = False
    metrics: List[QualityMetric] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class CertificationResult(BaseModel):
    project_id: str
    passed: bool = False
    is_certified: bool = False
    status: str = "NOT_EXECUTED"
    tier: str = "NONE"
    score: float = 0.0
    issues: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    feedback: Optional[str] = None
    details: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ReadinessResult(BaseModel):
    project_id: str
    ready: bool = False
    status: str = "NOT_EXECUTED"
    missing_requirements: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ReadinessGate:
    pass
