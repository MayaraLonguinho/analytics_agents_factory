# Agents

## Responsibility
Agentes especializados nativos do AAF (`DataAgent`, `DatabaseAgent`, `AnalyticsAgent`, `TestingAgent`, `DocumentationAgent`, etc.). Executam tarefas combinando raciocínio, Skills granulares, MCPs e chamadas ao LLM Gateway sob diretrizes do Brain.

## Path
`a_platform/g_agents/`

## Inputs
[[Project Factory]], [[Repair Loop]]

## Outputs
[[Artifact]]

## Integrations
- [[Skills]]
- [[MCPs]]
- [[Brain]]
- [[LLM Gateway]]
- [[Artifact]]

## Failure behavior
Lança exceção de execução capturada pelo Orchestrator e enviada ao [[Repair Loop]].
