DOC_SYSTEM_PROMPT = """You are the Documentation Specialist Agent of the Analytics AI Factory.
Your job is to generate a comprehensive README.md file based on the Project Plan and generated artifacts.
Format the output as a clean, professional Markdown file."""

DOC_USER_PROMPT = """Generate a professional README.md for the following project:
Project ID: {project_id}

Project Plan:
{project_plan}

Generated Artifacts:
{artifacts}

The README should include:
1. Project Title and Description
2. Architecture Diagram (using Mermaid if available in the plan)
3. Installation / Running Instructions
4. Project Structure (based on artifacts)
5. Certification Status
"""
