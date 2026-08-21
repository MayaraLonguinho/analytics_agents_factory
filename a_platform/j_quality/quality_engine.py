from typing import Dict, Any
from a_platform.j_quality.linters import Linter
from a_platform.j_quality.security_scanner import SecurityScanner

class QualityEngine:
    def __init__(self):
        self.linter = Linter()
        self.scanner = SecurityScanner()

    def evaluate(self, project_dir: str) -> Dict[str, Any]:
        lint_result = self.linter.run_linter(project_dir)
        sec_result = self.scanner.run_scan(project_dir)
        
        passed = lint_result["passed"] and sec_result["passed"]
        issues = []
        if not lint_result["passed"]:
            issues.append(f"Lint issues: {lint_result.get('issues')}")
        if not sec_result["passed"]:
            issues.append(f"Security issues: {sec_result.get('issues')}")
            
        return {
            "passed": passed,
            "issues": issues,
            "lint_score": 100 if lint_result["passed"] else 50,
            "sec_score": 100 if sec_result["passed"] else 50,
            "arch_score": 100
        }
