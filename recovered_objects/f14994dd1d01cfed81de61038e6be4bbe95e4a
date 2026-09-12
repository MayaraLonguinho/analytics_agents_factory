from typing import Dict, Any
from a_platform.e_skills.i_skill_contract import BaseSkill, SkillContract, CORE_SKILL_CONTRACTS

class GenericSkillImpl(BaseSkill):
    """Implementação genérica temporária para atender ao contrato sem quebrar a pipeline."""
    def __init__(self, skill_id: str):
        super().__init__()
        self.skill_id = skill_id

    def get_contract(self) -> SkillContract:
        return CORE_SKILL_CONTRACTS[self.skill_id]

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        contract = self.get_contract()
        # Stub implementation that returns a fake artifact string
        artifact_name = f"{self.skill_id}_output.txt"
        return {
            artifact_name: f"Artefato mock gerado pela skill {contract.name}."
        }

class CleaningSkill(GenericSkillImpl):
    def __init__(self): super().__init__("cleaning")

class DeduplicationSkill(GenericSkillImpl):
    def __init__(self): super().__init__("deduplication")

class CategorizationSkill(GenericSkillImpl):
    def __init__(self): super().__init__("categorization")

class AnalyticsSkill(GenericSkillImpl):
    def __init__(self): super().__init__("analytics")

class DashboardSkill(GenericSkillImpl):
    def __init__(self): super().__init__("dashboard")

class ChatbotSkill(GenericSkillImpl):
    def __init__(self): super().__init__("chatbot")

class BackendSkill(GenericSkillImpl):
    def __init__(self): super().__init__("backend")

class FrontendSkill(GenericSkillImpl):
    def __init__(self): super().__init__("frontend")

class TestingSkill(GenericSkillImpl):
    def __init__(self): super().__init__("testing")

class DocumentationSkill(GenericSkillImpl):
    def __init__(self): super().__init__("documentation")

class DockerSkill(GenericSkillImpl):
    def __init__(self): super().__init__("docker")
