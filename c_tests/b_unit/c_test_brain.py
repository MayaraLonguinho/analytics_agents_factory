import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.c_brain.h_brain import Brain

def test_brain_retrieval():
    b = Brain()
    knowledge = b.retrieve_relevant_knowledge({"domain": "analytics"})
    assert isinstance(knowledge, dict)
    assert "architecture" in knowledge
