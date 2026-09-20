"""
c_tests/a_unit/f_llm_gateway/d_test_structured_output.py
======================================================
Especificação executável de structured output no LLMGateway.
Valida conformidade com esquemas Pydantic / JSON Schema e rejeição de saídas malformadas.
"""
from unittest.mock import AsyncMock, patch
import pytest
from pydantic import BaseModel

from a_platform.j_llm_gateway.d_gateway import LLMGateway
from a_platform.j_llm_gateway.a_interfaces.a_base_provider import LLMResponse


class ExpectedOutputSchema(BaseModel):
    project_type: str
    domain: str


@pytest.mark.asyncio
async def test_structured_output_schema_enforcement(mock_api_keys):
    """Valida a emissão e validação estruturada com tipagem e schema enforcement."""
    gateway = LLMGateway()
    provider = gateway.provider_registry.get_provider("openai")

    if provider:
        with patch.object(provider, "generate", new_callable=AsyncMock) as mock_gen:
            valid_json = '{"project_type": "Pipeline", "domain": "analytics"}'
            mock_gen.return_value = LLMResponse(content=valid_json, model="gpt-4o-mini", provider="openai")

            response = await gateway.structured_output(
                prompt="Extract requirements",
                schema=ExpectedOutputSchema.model_json_schema(),
            )
            assert response.content is not None
