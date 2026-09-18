# Roteiro de Demonstração (Technical Presentation)

Este guia orienta a demonstração técnica das capacidades, garantias de segurança e arquitetura modular da **Analytics Agents Factory (AAF)** para equipes técnicas e stakeholders.

## Roteiro de Apresentação

### 1. Invocação via CLI Oficial

Demonstre a inicialização da esteira oficial utilizando a interface CLI suportada:

```bash
python f_cli/a_main.py start --project-id "demo_vendas" --prompt "Criar script de ingestão Python conectando a uma base CSV de vendas, tratando nulos e gravando em SQLite com suíte de testes pytest" --dataset "./b_input/c_dados_vendas.csv"
```

Destaque a separação estrita de responsabilidades: o chat da IDE atua apenas como canal de mensagens; todo o processamento é conduzido autonomamente pelos agentes internos do AAF.

### 2. O Papel do Brain (SSOT) e Visualização no Obsidian

- Mostre que o `ArchitectureAgent` consulta as regras em `a_platform/c_brain/b_rules/` em vez de tomar decisões arbitrárias.
- Abra o repositório no Obsidian para ilustrar o grafo conceitual de conhecimento (`.obsidian/`), enfatizando que a visualização é passiva e que o SSOT reside no sistema de arquivos.

### 3. Planejamento e Preflight de Segurança

- Evidencie a geração do `ProjectPlan` pelo `PlannerAgent`.
- Mostre como a `CommandPolicy` realiza a checagem prévia (*preflight*) dos comandos de execução planejados, bloqueando binários não autorizados antes de qualquer execução.

### 4. Fabricação e Sandbox de MCP

- Acompanhe a execução dos agentes especializados instanciados sob demanda pela `AgentFactory`.
- Demonstre o `Filesystem MCP` gravando os arquivos gerados exclusivamente no diretório isolado `e_generated_projects/demo_vendas/`.

### 5. Runtime, Validação e Certificação

- Acompanhe a execução segura no `k_runtime` (`shell=False`).
- Demonstre a verificação rigorosa pelo `ValidationGate` e a extração de métricas reais pela `QualityEngine`.
- Destaque que a concessão final do selo `PROJECT READY` é condicionada à passagem real da suíte de testes e validação documental pelo `CertificationEngine`:

```
===============================================
🏆 PROJECT READY = YES (demo_vendas)
===============================================
```
