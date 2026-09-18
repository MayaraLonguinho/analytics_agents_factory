import logging
from typing import Dict, Any
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import QualityResult
from .b_code_quality import CodeQuality
from .c_security_quality import SecurityQuality
from .d_dependency_quality import DependencyQuality

logger = logging.getLogger(__name__)

class QualityEngine:
    def __init__(self):
        self.code_quality = CodeQuality()
        self.security_quality = SecurityQuality()
        self.dep_quality = DependencyQuality()

    def evaluate(self, request: ExecutionContext, validation_result: Dict[str, Any], runtime_result: Dict[str, Any]) -> QualityResult:
        if not validation_result or validation_result.get("status") != "PASSED":
            return QualityResult(status="FAILED", evidence="Validação anterior falhou.")
            
        if not runtime_result:
            return QualityResult(status="FAILED", evidence="Ausência de evidências de runtime (Execução nula).")

        # Verifica todos os gates rigorosamente. ABSENCE OF EVIDENCE = FAILURE
        cq_pass = self.code_quality.evaluate(runtime_result)
        sq_pass = self.security_quality.evaluate(runtime_result)
        dq_pass = self.dep_quality.evaluate(runtime_result)
        
        if not cq_pass:
            return QualityResult(status="FAILED", evidence="Code/Test Quality failed or missing tool execution.")
        if not sq_pass:
            return QualityResult(status="FAILED", evidence="Security Quality failed or missing tool execution.")
        if not dq_pass:
            return QualityResult(status="FAILED", evidence="Dependency Quality failed or missing tool execution.")

        return QualityResult(status="PASSED", evidence="Todos os Quality Gates aprovaram com evidências reais.")
