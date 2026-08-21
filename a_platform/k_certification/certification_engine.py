from a_platform.a_core.b_domain.certification import CertificationResult
from a_platform.i_validation.validation_gate import ValidationGate
from a_platform.j_quality.quality_engine import QualityEngine
from a_platform.k_certification.score_calculator import ScoreCalculator

class CertificationEngine:
    def __init__(self):
        self.validation_gate = ValidationGate()
        self.quality_engine = QualityEngine()
        self.calculator = ScoreCalculator()

    def certify_project(self, project_id: str, project_dir: str) -> CertificationResult:
        val_result = self.validation_gate.validate(project_dir)
        qual_result = self.quality_engine.evaluate(project_dir)
        
        score = self.calculator.calculate(val_result["is_valid"], qual_result)
        if score >= 95.0:
            tier = "PLATINUM"
            is_certified = True
        elif score >= 85.0:
            tier = "GOLD"
            is_certified = True
        elif score >= 75.0:
            tier = "SILVER"
            is_certified = True
        else:
            tier = "REJECTED"
            is_certified = False
            
        passed = is_certified
        
        all_issues = []
        if not val_result["is_valid"]:
            all_issues.append("Validation tests failed.")
        all_issues.extend(qual_result.get("issues", []))
        
        return CertificationResult(
            project_id=project_id,
            passed=passed,
            is_certified=is_certified,
            tier=tier,
            issues=all_issues,
            metrics={"final_score": score, "validation": val_result, "quality": qual_result},
            feedback=f"Project is certified as {tier}." if is_certified else "Project needs fixes."
        )
