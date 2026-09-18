# Brain

## Papel no Golden Path
Repositório central de conhecimento e políticas arquiteturais da fábrica. Recupera padrões analíticos recomendados, convenções de engenharia de dados, regras de persistência SQLite e diretrizes de integridade adequadas ao domínio do projeto.

## Posição no Fluxo
← **Anterior:** [[c_dataset_profiling|Dataset Profiling]]  
→ **Próximo:** [[e_architecture|Architecture]]

## Entrada e Saída
- **Entrada:** `domain`, `business_context` e `dataset_profile` consolidados.
- **Saída:** `request.brain_context` contendo as regras e padrões de domínio que guiarão a tomada de decisão técnica.

## Integrações e Contratos
- Componente: `a_platform/c_brain/g_brain.py`
- Registries: `DomainRegistry`, `RuleRegistry`, `PatternRegistry` e `KnowledgeRegistry`.

## Referência Técnica
Para detalhes da arquitetura do Brain e desacoplamento do motor de learning, consulte [[c_brain|Arquitetura do Brain]].
