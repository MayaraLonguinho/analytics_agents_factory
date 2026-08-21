import pytest
from pydantic import BaseModel
from a_platform.d_skills.skill_contract import BaseSkill
from a_platform.d_skills.registry import SkillRegistry

class DummyInput(BaseModel):
    data: str

class DummyOutput(BaseModel):
    result: str

class DummySkill(BaseSkill):
    @property
    def name(self) -> str:
        return "dummy_skill"
        
    @property
    def input_schema(self):
        return DummyInput
        
    @property
    def output_schema(self):
        return DummyOutput
        
    async def execute(self, input_data: DummyInput) -> DummyOutput:
        return DummyOutput(result=input_data.data)

def test_skill_registry():
    registry = SkillRegistry()
    registry.register(DummySkill)
    skill_cls = registry.get_skill("dummy_skill")
    assert skill_cls == DummySkill
