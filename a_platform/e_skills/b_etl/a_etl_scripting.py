import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.i_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class EtlScriptingSkill(BaseSkill):
    def __init__(self):
        super().__init__()
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)

        tool = context["data_processing_tool"]
        description = context.get("task_description", "")
        dataset_profile = context.get("dataset_profile", {})
        project_plan = context.get("project_plan", {})

        logger.info(f"[EtlScriptingSkill] Gerando script ETL para {tool} usando LLM")

        system_prompt = (
            "Você é um engenheiro de dados sênior especializado em ETL. "
            "Gere o script de ETL Python limpo, documentado, tipado e com tratamento de erros. "
            "Responda SOMENTE com o código do script. Não use markdown formatting (```python) na resposta."
        )
        user_prompt = (
            f"Ferramenta: {tool}\nDescrição: {description}\n"
            f"Dataset Profile: {dataset_profile}\nPlan: {project_plan}"
        )

        llm_response = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)

        if not llm_response.content:
            msg = "[EtlScriptingSkill] LLM retornou conteúdo vazio."
            logger.error(msg)
            raise ValueError(msg)

        code_text = llm_response.content
        code_text = re.sub(r'^```[\w]*\n', '', code_text, flags=re.MULTILINE)
        code_text = re.sub(r'```$', '', code_text, flags=re.MULTILINE).strip()

        result = {"etl.py": code_text}
        self.validate_output(result)
        return result
