# Estratégia de Testes (Testing Strategy)

> **Documentação Técnica Oficial — Pirâmide de Testes e Garantia de Qualidade da Plataforma**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[k_security_and_guardrails|Anterior: Segurança e Guardrails]] | [[m_obsidian_knowledge_graph|Próximo: Grafo de Conhecimento Obsidian]]

---

## 1. Distinção Fundamental: Testes da Plataforma vs. Testes do Projeto Gerado

A arquitetura do AAF estabelece uma separação categórica entre dois universos de teste:

| Escopo de Teste | Onde Reside | O que Testa | Quem Executa |
|---|---|---|---|
| **Testes da Plataforma AAF** | `c_tests/` | Testa o código-fonte da própria fábrica (contratos, agentes, roteador de skills, gateways, MCPs, orquestrador). | Desenvolvedores da plataforma e suítes de CI/CD do repositório AAF. |
| **Testes do Projeto Gerado** | `e_generated_projects/<id>/tests/` | Testa a lógica analítica do projeto fabricado para o usuário (pipelines ETL, schemas SQL, agregações, integridade de dados). | O `RuntimeEngine` da plataforma durante a fase de execução do Golden Path. |

---

## 2. A Pirâmide de Testes da Plataforma (`c_tests/`)

A suíte de testes da plataforma está organizada em camadas em `c_tests/`:

```text
c_tests/
├── a_config/       # Testes de configurações globais, ambiente e .env
├── b_unit/         # Testes unitários isolados por componente
│   ├── a_test_contracts.py           # Contratos Pydantic e DTOs
│   ├── b_test_config_and_session.py  # Settings e StateManager
│   ├── c_test_brain.py               # Regras e recuperação do Brain
│   ├── d_test_decisions.py           # Registro e leitura de ADRs
│   ├── e_test_skills_and_registry.py # Contratos de skills e registro
│   ├── f_test_agents_and_factory.py  # Instanciação de agentes e factory
│   ├── g_test_mcp_and_executor.py    # Sandbox MCP e executor
│   └── h_test_gateway.py             # LLM Gateway e OpenAI Provider
├── c_integration/  # Testes de integração entre múltiplos componentes
├── d_validation/   # Testes dos gates de validação e compilação
└── e_end_to_end/   # Testes de ponta a ponta do pipeline completo (E2E)
```

---

## 3. Responsabilidades de Cada Camada de Teste

### 3.1 Camada Unitária (`c_tests/b_unit/`)
- **Objetivo:** Provar o comportamento atômico de classes, funções e modelos isolados, sem dependência de I/O externo ou chamadas reais de rede;
- **O que Deve Provar:**
  - Validação estrita de schemas em `b_contracts/`;
  - Serialização e desserialização de checkpoints no `StateManager`;
  - Roteamento correto e ordenação topológica no `SkillRouter`;
  - Instanciação dinâmica na `AgentFactory`;
  - Sanitização de caminhos na `PathPolicy` e de comandos na `CommandPolicy`.

### 3.2 Camada de Integração (`c_tests/c_integration/`)
- **Objetivo:** Provar a comunicação e a transição de dados entre dois ou mais subsistemas integrados;
- **O que Deve Provar:**
  - Interação entre `ProjectFactory` e `AgentFactory` despachando tarefas;
  - Gravação de artefatos via `ArtifactMaterializer` e validação pelo `ValidationGate`;
  - Execução segura pelo `RuntimeEngine` e consumo de evidências pelo `QualityEngine`.

### 3.3 Camada de Validação de Gates (`c_tests/d_validation/`)
- **Objetivo:** Provar que os gates de auditoria (`ValidationGate`, `QualityEngine`, `CertificationEngine`) detectam e reprovam anomalias reais com precisão;
- **O que Deve Provar:**
  - Reprovação quando um arquivo obrigatório estiver ausente;
  - Reprovação quando `py_compile` detectar erro de sintaxe Python;
  - Reprovação quando o comando do runtime retornar exit code != 0;
  - Reprovação quando o `bandit` detectar violação de segurança.

### 3.4 Camada de Ponta a Ponta (`c_tests/e_end_to_end/`)
- **Objetivo:** Provar a jornada completa do Golden Path, simulando a requisição de um usuário desde o prompt até a entrega do projeto com status `PROJECT READY = YES`.

---

## 4. Governança de Execução de Testes para Agentes da IDE

Conforme consagrado na Constituição Normativa (`.agents/a_AGENT.md`):
- **Proibição de Execução Arbitrária:** Agentes de desenvolvimento e agentes da IDE **NÃO devem disparar testes automatizados sem instrução explícita do desenvolvedor** durante etapas exclusivamente normativas ou documentais;
- **Integridade de Evidências:** É proibido modificar os testes para forçar passagem ou criar mocks temporários no código da fábrica apenas para simular sucesso de suíte.

---

## 5. Target Contract vs. Current Implementation Status

- **Target Contract:** Suíte E2E automatizada completa integrada com testes de mutação e cobertura mínima global de 85% em todas as camadas da fábrica.
- **Current Implementation Status:** Os testes unitários das camadas essenciais (`b_unit/`) estão implementados. A execução da esteira E2E completa encontra-se em fase de consolidação e estabilização de dependências de ambiente.

---

## Navegação

- Documento anterior: [[k_security_and_guardrails|Segurança e Guardrails]]
- Próximo passo técnico: [[m_obsidian_knowledge_graph|Grafo de Conhecimento Obsidian]]
- Visão operacional: [[j_operational_use|Uso Operacional]]
