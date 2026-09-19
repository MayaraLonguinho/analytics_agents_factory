import logging
import json
import re
import asyncio
import inspect
import uuid
from typing import Dict, Any, List

from a_platform.j_llm_gateway.d_gateway import LLMGateway
from a_platform.f_mcps.d_registry.b_executor import MCPExecutor
from a_platform.e_skills.h_registry.a_skill_registry import SkillRegistry
from a_platform.e_skills.skill_router import SkillRouter
from a_platform.b_contracts import ProjectTask as ProjectTask
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts import Artifact

logger = logging.getLogger(__name__)


class SkillExecutionError(RuntimeError):
    """Raised when a required skill is unavailable or fails. Always fatal for the task."""
    pass


class BaseAgent:
    def __init__(self, name: str, gateway: LLMGateway, mcp: MCPExecutor, skills: SkillRegistry):
        self.name = name
        self.gateway = gateway
        self.mcp = mcp
        self.skills = skills
        self.router = SkillRouter()

    def execute_task(self, task: ProjectTask, request: ExecutionContext) -> List[Artifact]:
        logger.info(f"[{self.name}] Iniciando task: {task.name}")
        artifacts: List[Artifact] = []

        # 1. Preparar contexto base
        arch = request.architecture_decision or {}
        discovery = request.discovery_data or {}
        base_context: Dict[str, Any] = {
            "domain": discovery.get("domain", "analytics"),
            "architecture": arch,
            "task_description": task.description,
            "dataset_path": request.dataset_path,
            "database_technology": arch.get("database_technology", "PostgreSQL"),
            "data_processing_tool": arch.get("data_processing", "Pandas"),
            "target_table": "main_table",
            "script_name": f"{self.name}_output.py",
            "schema_definition": "CREATE TABLE auto_generated (id INT);",
        }

        # 2. Determinar skills a executar (via required_skills ou roteamento multi-skill por capabilities/preferred_skills)
        skills_to_execute = list(task.required_skills)
        caps = task.get_all_capabilities() if hasattr(task, "get_all_capabilities") else list(getattr(task, "capabilities", []))
        if not caps and getattr(task, "capability", None):
            caps = [task.capability]

        prefs = task.get_all_preferred_skills() if hasattr(task, "get_all_preferred_skills") else list(getattr(task, "preferred_skills", []))
        if not prefs and getattr(task, "preferred_skill", None):
            prefs = [task.preferred_skill]

        if not skills_to_execute and (caps or prefs):
            try:
                selection = self.router.route_selection(
                    agent_name=self.name,
                    capabilities=caps,
                    preferred_skills=prefs,
                    task_description=task.description,
                    domain_name=base_context.get("domain")
                )
                skills_to_execute = selection.skill_ids
                logger.info(f"[{self.name}] Roteamento multi-skill selecionou {len(skills_to_execute)} skills para task '{task.name}': {skills_to_execute}")
            except Exception as e:
                logger.error(f"[{self.name}] Falha ao rotear capabilities da task: {e}")
                raise SkillExecutionError(str(e)) from e

        # Executar Skills via SkillRegistry (única autoridade de resolução operacional).
        # Qualquer falha é fatal — interrompe a Task imediatamente.
        for skill_name in skills_to_execute:
            skill_instance = self.skills.get_skill(skill_name)
            if skill_instance is None:
                msg = (
                    f"[{self.name}] Skill obrigatória '{skill_name}' não está registrada "
                    f"no SkillRegistry. Task '{task.name}' interrompida."
                )
                logger.error(msg)
                raise SkillExecutionError(msg)

            logger.info(f"[{self.name}] Executando skill obrigatória: {skill_name}")
            res = self.skills.run_skill(skill_name, base_context)

            if not res.get("success"):
                error_detail = res.get("error", "<sem detalhe>")
                msg = (
                    f"[{self.name}] Skill obrigatória '{skill_name}' falhou: "
                    f"{error_detail}. Task '{task.name}' interrompida."
                )
                logger.error(msg)
                raise SkillExecutionError(msg)

            art_name = res.get("artifact", f"{skill_name}_output.txt")
            content = res.get("content", "")
            artifacts.append(
                Artifact(
                    identity=str(uuid.uuid4()),
                    name=art_name,
                    path=art_name,
                    type="skill_output",
                    content=content,
                    metadata={"generator": "skill", "skill_name": skill_name},
                    producer=self.name,
                )
            )
            logger.info(f"[{self.name}] Skill '{skill_name}' gerou artefato '{art_name}'")

        # 3. Invocar MCPs requeridos (falha em MCP é sempre fatal)
        for mcp_name in getattr(task, "required_mcps", []):
            try:
                mcp_res = self.mcp.execute(mcp_name, payload=base_context)
                if mcp_res.get("status") not in ("ok", "PASSED"):
                    raise ValueError(f"MCP '{mcp_name}' retornou status inesperado: {mcp_res}")
                logger.info(f"[{self.name}] MCP '{mcp_name}' executado com sucesso.")
            except Exception as e:
                logger.error(f"[{self.name}] Falha fatal no MCP '{mcp_name}': {e}")
                raise RuntimeError(f"Falha na dependência MCP obrigatória: {mcp_name}") from e

        # 4. Invocar LLM para artefatos declarados em expected_artifacts que não
        #    foram cobertos por nenhuma Skill acima.
        generated_names = {a.name for a in artifacts}
        missing_artifacts = [
            ea for ea in getattr(task, "expected_artifacts", [])
            if ea not in generated_names
        ]

        for art in missing_artifacts:
            prompt = (
                f"Gere código final para '{task.name}' no contexto de "
                f"{arch.get('architecture_pattern', 'modular_monolith')}. "
                f"Deve produzir o arquivo: {art}"
            )
            try:
                if inspect.iscoroutinefunction(self.gateway.generate):
                    llm_resp = asyncio.run(
                        self.gateway.generate(
                            prompt,
                            system_prompt=f"Você é o {self.name}",
                            model_preference="openai",
                        )
                    )
                else:
                    llm_resp = self.gateway.generate(
                        prompt,
                        system_prompt=f"Você é o {self.name}",
                        model_preference="openai",
                    )
            except Exception as e:
                logger.error(f"[{self.name}] LLM falhou ao gerar '{art}': {e}")
                raise RuntimeError(f"LLM não conseguiu gerar artefato obrigatório '{art}'") from e

            if not llm_resp.content:
                msg = f"[{self.name}] LLM retornou conteúdo vazio para '{art}'. Task abortada."
                logger.error(msg)
                raise RuntimeError(msg)

            artifacts.append(
                Artifact(
                    identity=str(uuid.uuid4()),
                    name=art,
                    path=art,
                    type="source_code",
                    content=llm_resp.content,
                    metadata={"generator": "llm", "agent_name": self.name},
                    producer=self.name,
                )
            )

        logger.info(
            f"[{self.name}] ProjectTask '{task.name}' concluída. {len(artifacts)} artefatos gerados."
        )
        return artifacts
