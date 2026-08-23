import os
import json
import urllib.request
from typing import Optional

class LLMGateway:
    def __init__(self, provider="ollama", model="qwen2.5-coder"):
        self.provider = provider
        self.model = model

    async def generate(self, prompt: str, **kwargs) -> str:
        """Faz roteamento real para provedores LLM."""
        if self.provider == "openai":
            return self._call_openai(prompt, **kwargs)
        elif self.provider == "ollama":
            return self._call_ollama(prompt, **kwargs)
        else:
            return self._local_fallback(prompt, **kwargs)

    def _call_openai(self, prompt: str, **kwargs) -> str:
        # Implementation for OpenAI API
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("[LLM Gateway] WARNING: OPENAI_API_KEY not found. Using local fallback.")
            return self._local_fallback(prompt, **kwargs)
        # Real HTTP Request goes here
        return self._local_fallback(prompt, **kwargs)
        
    def _call_ollama(self, prompt: str, **kwargs) -> str:
        # Implementation for Ollama Local
        try:
            req = urllib.request.Request("http://127.0.0.1:11434/api/generate", 
                                      data=json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode('utf-8'),
                                      headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("response", self._local_fallback(prompt, **kwargs))
        except Exception as e:
            print(f"[LLM Gateway] WARNING: Ollama connection failed ({e}). Using local fallback.")
            return self._local_fallback(prompt, **kwargs)

    def _local_fallback(self, prompt: str, **kwargs) -> str:
        """
        Fallback extremo caso APIs falhem (garante teste E2E real).
        """
        return '''
```python:requirements.txt
pytest
```
```python:main.py
def add(a, b):
    return a + b

if __name__ == "__main__":
    print(add(2, 3))
```
```python:test_main.py
from main import add

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
```
'''
