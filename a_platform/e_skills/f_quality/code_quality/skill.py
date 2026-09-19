import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class CodeQualitySkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="code-quality",
            name="Code Quality Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Testes unitários e qualidade de código com pytest")
        plan = context.get("project_plan", {})

        system_prompt = (
            "Você é um engenheiro de QA especialista em testes Python e pytest. "
            "Gere uma suíte de testes limpa e executável 'test_pipeline.py' cobrindo o pipeline, "
            "transformações e asserts fundamentais com fixtures adequadas. "
            "Responda SOMENTE com o código Python, sem markdown formatting (```python)."
        )
        user_prompt = f"Descrição: {description}\nPlano: {plan}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        code = resp.content or ""
        code = re.sub(r'^```[\w]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'```$', '', code, flags=re.MULTILINE).strip()

        result = {"test_pipeline.py": code}
        self.validate_output(result)
        return result
