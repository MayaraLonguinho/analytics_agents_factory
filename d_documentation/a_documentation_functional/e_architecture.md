# Architecture

## Papel no Golden Path
Definição estruturada da arquitetura tecnológica do projeto gerado. O `ArchitectureAgent` seleciona a pilha técnica (Modular Monolith, Python, SQLite para persistência, pytest para testes automatizados) e estabelece as restrições obrigatórias de execução.

## Posição no Fluxo
← **Anterior:** [[d_brain|Brain]]  
→ **Próximo:** [[f_planner|Planner]]

## Entrada e Saída
- **Entrada:** `request.brain_context` e `request.discovery_data`.
- **Saída:** `request.architecture_decision` com o padrão arquitetural, tecnologia de banco, ferramenta de processamento e componentes a serem gerados.

## Integrações e Contratos
- Componente: `a_platform/g_agents/c_architecture/a_architecture_agent.py`
- LLM Gateway: `a_platform/j_llm_gateway/d_gateway.py`

## Referência Técnica
Para as diretrizes técnicas do Monolito Modular e decisões estruturais, consulte [[a_architecture|Arquitetura Geral]].
