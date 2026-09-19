"""
SkillIndex — Catálogo canônico compacto para descoberta e consulta de Skills.
Carrega e consulta a_platform/e_skills/skill_index.yaml.
Não instancia, não executa e não substitui o SkillRegistry.
"""
import os
import logging
from typing import Dict, Any, List, Optional
import yaml

logger = logging.getLogger(__name__)

class SkillMetadata:
    def __init__(self, skill_id: str, data: Dict[str, Any]):
        self.skill_id = skill_id
        self.category = data.get("category", "")
        self.description = data.get("description", "")
        self.location = data.get("location", "")
        self.capabilities = data.get("capabilities", [])
        self.triggers = data.get("triggers", [])
        self.allowed_agents = data.get("allowed_agents", [])
        self.depends_on = data.get("depends_on", [])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "category": self.category,
            "description": self.description,
            "location": self.location,
            "capabilities": self.capabilities,
            "triggers": self.triggers,
            "allowed_agents": self.allowed_agents,
            "depends_on": self.depends_on,
        }

    def __repr__(self) -> str:
        return f"<SkillMetadata id={self.skill_id} category={self.category} depends_on={self.depends_on}>"


class SkillIndex:
    """
    Índice canônico de descoberta de Skills.
    Responsável apenas por indexar metadados compactos.
    """
    _instance: Optional["SkillIndex"] = None

    def __init__(self, yaml_path: Optional[str] = None):
        if not yaml_path:
            yaml_path = os.path.join(os.path.dirname(__file__), "skill_index.yaml")
        self.yaml_path = yaml_path
        self._skills: Dict[str, SkillMetadata] = {}
        self.load()

    def load(self) -> None:
        """Carrega o catálogo yaml para a memória."""
        if not os.path.exists(self.yaml_path):
            logger.warning(f"[SkillIndex] Arquivo de catálogo não encontrado: {self.yaml_path}")
            return

        with open(self.yaml_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        skills_dict = raw.get("skills", {})
        self._skills = {
            s_id: SkillMetadata(s_id, meta)
            for s_id, meta in skills_dict.items()
        }
        logger.info(f"[SkillIndex] Carregadas {len(self._skills)} skills do índice.")

    def get(self, skill_id: str) -> Optional[SkillMetadata]:
        """Obtém metadados de uma skill pelo ID."""
        if skill_id in self._skills:
            return self._skills[skill_id]
        normalized = skill_id.replace("_", "-")
        return self._skills.get(normalized)

    def list_metadata(self) -> List[Dict[str, Any]]:
        """Retorna lista com metadados de todas as skills registradas."""
        return [s.to_dict() for s in self._skills.values()]

    def find_by_capability(self, capability: str) -> List[SkillMetadata]:
        """Busca skills que possuem a capability exata ou coincidem com o ID."""
        cap_norm = capability.strip().lower().replace("_", "-")
        results = []
        for s in self._skills.values():
            s_norm = s.skill_id.lower().replace("_", "-")
            if s_norm == cap_norm:
                results.append(s)
            elif any(c.lower().replace("_", "-") == cap_norm for c in s.capabilities):
                results.append(s)
        return results

    def find_by_category(self, category: str) -> List[SkillMetadata]:
        """Busca skills de uma categoria específica."""
        cat_norm = category.strip().lower()
        return [s for s in self._skills.values() if s.category.lower() == cat_norm]

    def find_allowed_for_agent(self, agent_name: str) -> List[SkillMetadata]:
        """Lista skills autorizadas para determinado agente."""
        agent_norm = agent_name.strip()
        return [s for s in self._skills.values() if agent_norm in s.allowed_agents]

    @classmethod
    def get_instance(cls) -> "SkillIndex":
        if cls._instance is None:
            cls._instance = SkillIndex()
        return cls._instance
