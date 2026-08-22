import os
import re

replacements = {
    r'c_agents\.a_discovery_agent': 'a_platform.c_agents.b_discovery',
    r'c_agents\.b_architecture_agent': 'a_platform.c_agents.c_architecture',
    r'c_agents\.c_planner_agent': 'a_platform.c_agents.d_planner',
    r'c_agents\.d_etl_agent': 'a_platform.c_agents.e_data',
    r'c_agents\.e_db_agent': 'a_platform.c_agents.f_database',
    r'c_agents\.f_backend_agent': 'a_platform.c_agents.g_backend',
    r'c_agents\.g_frontend_agent': 'a_platform.c_agents.h_frontend',
    r'c_agents\.h_devops_agent': 'a_platform.c_agents.j_infrastructure',
    r'c_agents\.i_qa_agent': 'a_platform.c_agents.k_testing',
    r'c_agents\.j_documentation_agent': 'a_platform.c_agents.l_documentation',
    r'a_platform\.g_materializer': 'a_platform.g_factory.d_artifact_materializer',
}

def process_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

    new_content = content
    for pattern, replacement in replacements.items():
        new_content = re.sub(pattern, replacement, new_content)

    if new_content != content:
        with open(filepath, 'w') as file:
            file.write(new_content)
        print(f"Updated imports in {filepath}")

for root, _, files in os.walk('.'):
    if '.venv' in root or '.git' in root or '__pycache__' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            process_file(os.path.join(root, file))

