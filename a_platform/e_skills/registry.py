from typing import Dict, Type
from a_platform.d_skills.skill_contract import BaseSkill

class SkillRegistry:
    def __init__(self):
        self.skills: Dict[str, Type[BaseSkill]] = {}
        
    def register(self, skill_cls: Type[BaseSkill]):
        # Mock instance to get name
        instance = skill_cls()
        self.skills[instance.name] = skill_cls
        
    def get_skill(self, name: str) -> Type[BaseSkill]:
        return self.skills.get(name)
