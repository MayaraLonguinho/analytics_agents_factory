class ScoreCalculator:
    def calculate(self, validation_passed: bool, quality_metrics: dict) -> float:
        base_score = 0
        if validation_passed:
            base_score += 40
            
        lint_score = quality_metrics.get("lint_score", 0)
        arch_score = quality_metrics.get("arch_score", 0)
        sec_score = quality_metrics.get("sec_score", 0)
        
        base_score += (lint_score * 0.3)
        base_score += (arch_score * 0.15)
        base_score += (sec_score * 0.15)
        
        return base_score
