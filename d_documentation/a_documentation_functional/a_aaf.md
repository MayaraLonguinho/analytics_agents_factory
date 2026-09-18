# AAF — Analytics Agents Factory

## Papel no Golden Path
Ponto central e de entrada da plataforma Analytics Agents Factory. Recebe a solicitação do usuário, inicializa o contexto unificado de execução e aciona o motor de orquestração serial (`MasterOrchestrator`).

## Posição no Fluxo
**Início do Golden Path**  
→ **Próximo:** [[b_discovery|Discovery]]

## Entrada e Saída
- **Entrada:** Solicitação do usuário via CLI (`aaf start`) ou interface de chat, contendo a descrição do projeto e caminho opcional do dataset.
- **Saída:** `ExecutionContext` tipado inicializado com identificador único de projeto (`project_id`).

## Integrações e Contratos
- Entrypoint: `f_cli/a_main.py`
- Adaptador: `a_platform/b_contracts/z_interfaces/a_ide_adapter.py`
- Orquestrador: `a_platform/o_orchestration/a_orchestrator.py`

## Referência Técnica
Para detalhes de arquitetura do monolito modular e comandos operacionais, consulte [[a_architecture|Arquitetura Geral]] e [[b_operation|Operação da Plataforma]].
