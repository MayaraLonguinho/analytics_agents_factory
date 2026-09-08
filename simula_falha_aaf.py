import os
import sys
from unittest.mock import patch, MagicMock

sys.modules['a_platform.g_llm_gateway.gateway'] = MagicMock()
sys.modules['a_platform.d_agents.agent_factory'] = MagicMock()
sys.modules['a_platform.h_factory.a_project_factory.project_factory'] = MagicMock()

from a_platform.b_interfaces.a_ide.adapter import IDEAdapter

def simular_cenario():
    print("--- INICIANDO SIMULACAO DO IDE AGENT ---")
    print("O IDE Agent não tentará codificar. Ele invoca o IDEAdapter...\n")
    
    adapter = IDEAdapter()
    
    # Mocking o LLM do DiscoveryAgent para retornar status de Needs Input ou Falha Semântica (porque não mockamos os responses)
    # A resposta será devolvida pelo Orchestrator como DTO Failed
    response = adapter.create_project(
        prompt="Gere um sistema bancário de ponta a ponta sem dataset.",
        dataset_path=None,
        domain="fintech" 
    )
    
    print("--- RETORNO DO IDE ADAPTER ---")
    print(f"Success: {response.success}")
    print(f"Status: {response.status}")
    print(f"Error Diagnostic: {response.error}")
    
    print("\n--- COMPORTAMENTO DO IDE AGENT ---")
    if not response.success:
        print("IDE Agent: 'Houve uma falha na Analytics AI Factory durante a execução.'")
        print(f"IDE Agent: 'Diagnóstico retornado: {response.error}'")
        print("IDE Agent: (FIM DA INTERAÇÃO. NENHUM CÓDIGO FOI GERADO MANUALMENTE)")

if __name__ == "__main__":
    simular_cenario()
