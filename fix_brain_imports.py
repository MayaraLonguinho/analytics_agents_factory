import os

def replace_in_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Replaced in {filepath}")

replace_in_file('c_tests/unit/brain/test_brain_learning.py', 'KnowledgeItem', 'Dict[str, Any]')
replace_in_file('c_tests/unit/brain/test_brain_learning.py', 'from a_platform.n_learning.brain_updater import BrainUpdater, Dict[str, Any]', 'from a_platform.n_learning.brain_updater import BrainUpdater\nfrom typing import Dict, Any')

replace_in_file('c_tests/unit/test_brain.py', 'from a_platform.c_brain.f_registry.knowledge_registry import KnowledgeRegistry', 'from a_platform.c_brain.f_registry.knowledge_registry import BrainRegistry as KnowledgeRegistry')
