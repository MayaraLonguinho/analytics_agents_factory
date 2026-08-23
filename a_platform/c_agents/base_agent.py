import logging
import os
from typing import Dict, Any

from a_platform.f_llm_gateway.gateway import LLMGateway
from a_platform.e_mcp.mcp_executor import MCPExecutor
from a_platform.d_skills.skill_registry import SkillRegistry
from a_platform.a_core.b_domain.project_plan import Task
from a_platform.a_core.b_domain.project_request import ProjectRequest

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, name: str, gateway: LLMGateway, mcp: MCPExecutor, skills: SkillRegistry):
        self.name = name
        self.gateway = gateway
        self.mcp = mcp
        self.skills = skills

    def execute_task(self, task: Task, request: ProjectRequest) -> bool:
        logger.info(f"[{self.name}] Iniciando task: {task.name}")
        
        # 1. Preparar contexto (Brain + Plan)
        context = {
            "domain": request.discovery_data.get("domain", "generic"),
            "architecture": request.architecture_decision,
            "task_description": task.description
        }
        
        project_dir = os.path.join(os.getcwd(), "e_generated_projects", request.project_id)
        os.makedirs(project_dir, exist_ok=True)
        
        # 2. Chamar Skills requeridas
        for skill_name in task.skills:
            res = self.skills.run_skill(skill_name, context)
            if res.get("success"):
                # Salvar o artefato gerado pela skill via MCP
                file_path = os.path.join(project_dir, res.get("artifact", "unknown.txt"))
                self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=res.get("content", ""))
                logger.info(f"[{self.name}] Skill {skill_name} gerou {file_path}")
            else:
                logger.warning(f"[{self.name}] Falha na skill {skill_name}: {res.get('error')}")

        # 3. Invocar LLM para complementar lógica se necessário
        prompt = f"Gere código base para {task.name} no contexto de {context['architecture'].get('architecture_pattern')}"
        llm_resp = self.gateway.generate_text(prompt, system_prompt=f"Você é o {self.name}", model_preference="openai")
        if llm_resp.get("success"):
            file_path = os.path.join(project_dir, f"{self.name}_output.py")
            self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=llm_resp.get("text"))
        else:
            logger.error(f"[{self.name}] Erro no LLM: {llm_resp.get('error')}")
            return False

        # 4. Usar ferramentas extras MCP (ex: init git)
        if "git_mcp" in task.mcps:
            self.mcp.execute_tool("git_mcp", command="init", cwd=project_dir)

        logger.info(f"[{self.name}] Task {task.name} concluída.")
        return True
