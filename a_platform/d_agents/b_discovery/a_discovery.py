"""IDE-agent facing discovery contract.

The IDE/LLM agent owns this conversation.  The Factory only accepts an approved
configuration, so no architectural choice is silently invented at generation.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional

DEFAULTS = {
    "project_name": "Analytics Project",
    "domain": "analytics",
    "objective": "Not specified",
    "data_source": "Not specified",
    "backend": "FastAPI",
    "frontend": "React + Vite",
    "database": "PostgreSQL",
    "infrastructure": "Docker",
    "authentication": "JWT",
    "analytics": "pandas",
    "etl": "None",
    "deployment": "Local",
    "security": "Standard",
    "testing": "pytest",
    "documentation": "README"
}

REQUIRED = (
    "project_name", "domain", "objective", "data_source", 
    "backend", "frontend", "database", "infrastructure", 
    "authentication", "analytics", "etl", "deployment", 
    "security", "testing", "documentation"
)

SIGNALS = {
    "backend": (("fastapi", "FastAPI"), ("flask", "Flask"), ("nest", "NestJS"), ("spring", "Spring Boot")),
    "frontend": (("react", "React + Vite"), ("vite", "React + Vite"), ("next", "Next.js"), ("angular", "Angular")),
    "database": (("postgres", "PostgreSQL"), ("mysql", "MySQL"), ("mongo", "MongoDB")),
    "infrastructure": (("docker", "Docker"), ("terraform", "Docker + Terraform"), ("kubernetes", "Kubernetes"), ("local", "Local")),
    "authentication": (("jwt", "JWT"), ("oauth", "OAuth2"), ("auth0", "Auth0")),
    "analytics": (("pandas", "pandas"), ("pyspark", "PySpark"), ("powerbi", "PowerBI")),
    "etl": (("airflow", "Airflow"), ("dbt", "dbt"), ("custom", "Custom Script")),
    "deployment": (("aws", "AWS"), ("gcp", "GCP"), ("azure", "Azure"), ("local", "Local")),
    "testing": (("pytest", "pytest"), ("unittest", "unittest"), ("jest", "Jest")),
}

@dataclass
class DiscoverySession:
    request: str
    answers: Dict[str, str] = field(default_factory=dict)
    domain: Optional[str] = None

    def __post_init__(self) -> None:
        self.answers.update({key: value for key, value in self._infer_from_request().items() if key not in self.answers})

    def _infer_from_request(self) -> Dict[str, str]:
        text = self.request.lower()
        inferred: Dict[str, str] = {}
        for field_name, options in SIGNALS.items():
            for token, value in options:
                if token in text:
                    inferred[field_name] = value
                    break
        return inferred

    def get_pending_questions(self) -> List[Dict[str, str]]:
        questions = []
        for key in REQUIRED:
            if key not in self.answers:
                default_val = DEFAULTS[key]
                questions.append({
                    "field": key,
                    "default": default_val,
                    "question": f"O campo '{key}' não foi especificado. O padrão é '{default_val}'. O que deseja fazer?"
                })
        return questions

    def next_question(self) -> Optional[Dict[str, str]]:
        pending = self.get_pending_questions()
        return pending[0] if pending else None

    def answer(self, field: str, value: Optional[str] = None) -> None:
        if field not in REQUIRED:
            raise ValueError(f"Unknown architecture decision: {field}")
        self.answers[field] = value or DEFAULTS[field]

    @property
    def pending_questions_count(self) -> int:
        return len(self.get_pending_questions())

    @property
    def ready(self) -> bool:
        return self.pending_questions_count == 0

    def approved_configuration(self) -> Dict[str, str]:
        if not self.ready:
            raise ValueError("Discovery is incomplete; generation is not authorized")
        return dict(self.answers)
