"""
Planner Agent Configuration
"""

from typing import Dict, Any


class PlannerConfig:
    """Configuração do Planner Agent."""

    def __init__(self):
        """Inicializa configuração padrão."""
        self.max_tasks: int = 100
        self.max_parallel_groups: int = 10
        self.enable_parallelism: bool = True
        self.default_agent: str = "general_agent"
        self.cost_estimation_factor: float = 1.0
        self.time_estimation_factor: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário."""
        return {
            "max_tasks": self.max_tasks,
            "max_parallel_groups": self.max_parallel_groups,
            "enable_parallelism": self.enable_parallelism,
            "default_agent": self.default_agent,
            "cost_estimation_factor": self.cost_estimation_factor,
            "time_estimation_factor": self.time_estimation_factor
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "PlannerConfig":
        """Cria configuração a partir de dicionário."""
        config = cls()
        config.max_tasks = config_dict.get("max_tasks", 100)
        config.max_parallel_groups = config_dict.get("max_parallel_groups", 10)
        config.enable_parallelism = config_dict.get("enable_parallelism", True)
        config.default_agent = config_dict.get("default_agent", "general_agent")
        config.cost_estimation_factor = config_dict.get("cost_estimation_factor", 1.0)
        config.time_estimation_factor = config_dict.get("time_estimation_factor", 1.0)
        return config
