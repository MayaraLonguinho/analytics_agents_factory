import pytest
from a_platform.f_llm_gateway.gateway import LLMGateway
from pydantic import BaseModel

class MockModel(BaseModel):
    pass

@pytest.mark.asyncio
async def test_llm_gateway_routing():
    gateway = LLMGateway()
    result = await gateway.generate("test prompt", complexity="high")
    assert result == "OpenAI mocked response"
    
    result = await gateway.generate("test prompt", complexity="low")
    assert result == "Ollama mocked response"

@pytest.mark.asyncio
async def test_llm_gateway_structured():
    gateway = LLMGateway()
    result = await gateway.generate_structured("test", MockModel, complexity="low")
    assert isinstance(result, MockModel)
