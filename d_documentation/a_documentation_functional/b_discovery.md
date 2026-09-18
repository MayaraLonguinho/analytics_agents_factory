# Discovery

## Papel no Golden Path
Fase de descoberta e levantamento de requisitos. O `DiscoveryAgent` extrai o domínio técnico canônico (`analytics` ou `data_engineering`), identifica objetivos de negócio e valida se há informações suficientes para projetar a solução. Quando restam dúvidas fundamentais, pausa o pipeline (`NEEDS_INPUT`) e persiste o estado em `h_runtime/state/` aguardando a resposta do usuário (limite estrito de 5 perguntas).

## Posição no Fluxo
← **Anterior:** [[a_aaf|AAF]]  
→ **Próximo:** [[c_dataset_profiling|Dataset Profiling]]

## Entrada e Saída
- **Entrada:** `ExecutionContext` contendo o prompt inicial e o contexto de negócio.
- **Saída:** `discovery_data` com domínio normalizado, requisitos refinados e status `COMPLETE`.

## Integrações e Contratos
- Componente: `a_platform/g_agents/b_discovery/a_discovery_agent.py`
- State Manager: `a_platform/b_contracts/j_state_manager.py` (armazenamento em `h_runtime/state/<project_id>.json`)

## Referência Técnica
Para o protocolo de pausa, retomada e comandos da CLI, consulte [[b_operation|Operação da Plataforma]].
