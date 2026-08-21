from pydantic_settings import BaseSettings

class GatewaySettings(BaseSettings):
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"

gateway_settings = GatewaySettings()
