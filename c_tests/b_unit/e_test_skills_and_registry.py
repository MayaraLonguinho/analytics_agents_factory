import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.e_skills.g_registry.j_skill_registry import SkillRegistry
from a_platform.e_skills.a_dataset.c_profiling.a_profiler import DatasetProfilingSkill

def test_skill_registry():
    registry = SkillRegistry()
    skill = registry.get_skill("dataset_profiling")
    assert isinstance(skill, DatasetProfilingSkill)

def test_dataset_profiling_skill_interface():
    skill = DatasetProfilingSkill()
    assert skill.__class__.__name__ == "DatasetProfilingSkill"
