import logging
import os
import yaml
import ast
import subprocess
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest

logger = logging.getLogger(__name__)

class CyclomaticComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_And(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_Or(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

class QualityEngine:
    """
    Quality Engine.
    Analisa qualidade estática e governança calculando métricas reais.
    """
    def __init__(self, thresholds_path: str = None):
        if not thresholds_path:
            thresholds_path = os.path.join(os.path.dirname(__file__), "thresholds.yaml")
        
        self.thresholds_path = thresholds_path
        self.metrics = {}
        self.passing_score = 60
        self.max_complexity = 10
        self._load_thresholds()

    def _load_thresholds(self):
        try:
            with open(self.thresholds_path, 'r') as f:
                data = yaml.safe_load(f)
                self.metrics = data.get("metrics", {})
                self.passing_score = data.get("passing_score", 60)
                self.max_complexity = data.get("max_complexity", 10)
        except Exception as e:
            logger.error(f"[QualityEngine] Falha ao carregar thresholds: {e}")
            self.metrics = {"linting_weight": 0.4, "architecture_weight": 0.3, "documentation_weight": 0.3}

    def run_quality(self, request: ProjectRequest) -> bool:
        domain = request.discovery_data.get("domain", "generic").lower()
        project_dir = os.path.abspath(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        
        logger.info(f"[QualityEngine] Avaliando projeto em {project_dir}")
        
        if not os.path.exists(project_dir):
            return False

        # Inicia pontuação zerada e ganha pontos
        linting_score = 0
        architecture_score = 0
        doc_score = 0
        
        py_files = []
        test_files = []
        for root, _, files in os.walk(project_dir):
            if "venv" in root: continue
            for f in files:
                if f.endswith(".py"):
                    full_path = os.path.join(root, f)
                    py_files.append(full_path)
                    if f.startswith("test_"):
                        test_files.append(full_path)
                    
        if not py_files:
            logger.warning("[QualityEngine] Nenhum arquivo .py encontrado no projeto.")
            return False

        # Avalia Linting via AST e Syntax
        syntax_errors = 0
        total_complexity = 0
        total_elements = 0
        documented_elements = 0
        
        for pf in py_files:
            try:
                with open(pf, "r") as code:
                    tree = ast.parse(code.read())
                    
                # Complexidade ciclomática
                visitor = CyclomaticComplexityVisitor()
                visitor.visit(tree)
                total_complexity += visitor.complexity
                
                # Check module docstring
                total_elements += 1
                if ast.get_docstring(tree):
                    documented_elements += 1
                    
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        total_elements += 1
                        if ast.get_docstring(node):
                            documented_elements += 1
                            
            except SyntaxError:
                syntax_errors += 1
            except Exception as e:
                logger.error(f"[QualityEngine] Erro ao analisar {pf}: {e}")
                syntax_errors += 1
                
        # Calcula scores
        linting_score = 100 if syntax_errors == 0 else max(0, 100 - (syntax_errors * 50))
        
        avg_complexity = total_complexity / len(py_files)
        if avg_complexity <= self.max_complexity:
            architecture_score = 100
        else:
            architecture_score = max(0, 100 - ((avg_complexity - self.max_complexity) * 10))
            
        if total_elements > 0:
            doc_score = int((documented_elements / total_elements) * 100)
        else:
            doc_score = 0
            
        # Penalidade severa se não houver testes quando requeridos?
        # O Quality Engine avalia a existência e cobertura.
        if len(test_files) == 0:
            logger.warning("[QualityEngine] Nenhum teste encontrado. Reduzindo architecture score.")
            architecture_score -= 30

        final_score = (
            linting_score * self.metrics.get("linting_weight", 0.4) +
            architecture_score * self.metrics.get("architecture_weight", 0.3) +
            doc_score * self.metrics.get("documentation_weight", 0.3)
        )
        
        request.metadata["quality_score"] = final_score
        
        if final_score >= self.passing_score and linting_score > 0:
            logger.info(f"[QualityEngine] Qualidade aprovada com score {final_score:.1f}")
            return True
        else:
            logger.error(f"[QualityEngine] Qualidade reprovada. Score: {final_score:.1f}, Linting: {linting_score}")
            return False
