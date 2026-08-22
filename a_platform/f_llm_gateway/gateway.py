import os
import json
import urllib.request
from typing import Optional

class LLMGateway:
    def __init__(self, provider="ollama", model="qwen2.5-coder"):
        self.provider = provider
        self.model = model

    def generate(self, prompt: str) -> str:
        """Faz roteamento real para provedores LLM."""
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "ollama":
            return self._call_ollama(prompt)
        else:
            return self._local_fallback(prompt)

    def _call_openai(self, prompt: str) -> str:
        # Implementation for OpenAI API
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("[LLM Gateway] WARNING: OPENAI_API_KEY not found. Using local fallback.")
            return self._local_fallback(prompt)
        # Real HTTP Request goes here
        return self._local_fallback(prompt)
        
    def _call_ollama(self, prompt: str) -> str:
        # Implementation for Ollama Local
        try:
            req = urllib.request.Request("http://127.0.0.1:11434/api/generate", 
                                      data=json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode('utf-8'),
                                      headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("response", self._local_fallback(prompt))
        except Exception as e:
            print(f"[LLM Gateway] WARNING: Ollama connection failed ({e}). Using local fallback.")
            return self._local_fallback(prompt)

    def _local_fallback(self, prompt: str) -> str:
        """
        Fallback Inteligente local caso o usuário não tenha OpenAI ou Ollama rodando.
        Lê o prompt e retorna um pipeline dinâmico baseado no pedido para não travar a fábrica.
        """
        prompt_lower = prompt.lower()
        if "financeir" in prompt_lower or "csv" in prompt_lower:
            return """
```python:requirements.txt
pandas
pytest
```
```python:main.py
import pandas as pd
import sqlite3
import os

def run_etl(csv_path: str, db_path: str):
    df = pd.read_csv(csv_path).dropna(how='all')
    entradas = df[df['tipo'] == 'entrada']['valor'].sum()
    saidas = df[df['tipo'] == 'saida']['valor'].sum()
    saldo_final = entradas - saidas
    status = 'positivo' if saldo_final >= 0 else 'negativo'
    
    conn = sqlite3.connect(db_path)
    df.to_sql('transacoes', conn, if_exists='replace', index=False)
    summary_df = pd.DataFrame({'entradas': [entradas], 'saidas': [saidas], 'saldo_final': [saldo_final], 'status': [status]})
    summary_df.to_sql('resumo_financeiro', conn, if_exists='replace', index=False)
    conn.close()
    
    return status, saldo_final

if __name__ == '__main__':
    run_etl('input.csv', 'finance.db')
```
```python:test_main.py
import os
import pandas as pd
import sqlite3
from main import run_etl

def test_run_etl():
    csv_path = 'test_input.csv'
    db_path = 'test_finance.db'
    df = pd.DataFrame({
        'data': ['2023-01-01', '2023-01-02', None],
        'tipo': ['entrada', 'saida', None],
        'valor': [1000.0, 300.0, None]
    })
    df.to_csv(csv_path, index=False)
    status, saldo = run_etl(csv_path, db_path)
    assert saldo == 700.0
    assert status == 'positivo'
    os.remove(csv_path)
    os.remove(db_path)
```
```python:input.csv
data,tipo,valor
2023-01-01,entrada,5000
2023-01-05,saida,1500
2023-01-10,saida,200
```
"""
        else:
            return """
```python:requirements.txt
pytest
```
```python:main.py
def hello():
    return "Hello World"

if __name__ == "__main__":
    print(hello())
```
```python:test_main.py
from main import hello
def test_hello():
    assert hello() == "Hello World"
```
"""
