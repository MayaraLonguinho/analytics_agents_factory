# Execução e Portões de Validação (Execution & Gates)

> **Documentação Funcional Oficial — Da Execução Real à Auditoria Multifacetada**  
> **Status:** Canônico / Normativo  
> **Navegação:** [[f_project_generation|Anterior: Geração de Projetos]] | [[h_repair_and_recovery|Próximo: Reparo e Recuperação]]

---

## 1. Princípio da Execução Real vs. Proibição de Mocks

No AAF, a geração de código **não é o fim da linha**, mas apenas o primeiro passo. A plataforma possui uma regra absoluta de engenharia:
> **"Nenhum projeto é entregue sem ser fisicamente executado em ambiente de runtime, e nenhum gate concede aprovação com base em presunção ou mocks."**

Mocks permanentes, flags booleanas forçadas (`passed = True` sem execução), supressão de stacktraces ou declarações de sucesso artificial (*fake success*) são terminantemente repudiados e considerados violações graves de arquitetura.

---

## 2. O Execution Runtime (`a_platform/k_runtime/`)

O **ProjectRuntime** (`RuntimeEngine`) é o motor encarregado de executar fisicamente os comandos planejados do projeto gerado dentro de seu diretório materializado (`e_generated_projects/<project_id>/`).

### 2.1 Características da Execução Segura
- **Subprocesso Isolado:** Disparo via `subprocess.Popen` com `shell=False` estrito;
- **Lista de Argumentos:** Argumentos passados como lista sanitizada (`["python", "src/pipeline.py"]`), impedindo injeção de comandos de terminal;
- **Timeout Rígido:** Cada comando possui timeout padrão de 120 segundos para prevenir deadlocks ou loops infinitos de processamento;
- **Conformidade com `CommandPolicy`:** Apenas comandos aprovados pelo preflight de segurança são autorizados a rodar.

### 2.2 Coleta Compulsória de Evidências Físicas
Para cada comando executado, o Runtime constrói uma instância de `CommandExecutionResult`:
- Código de retorno exato do processo (`return_code`);
- Saída padrão capturada (`stdout`);
- Saída de erro capturada (`stderr`);
- Tempo decorrido de execução em segundos;
- Arquivos gerados ou modificados em disco durante o comando.

Essas evidências são agregadas no `ExecutionResult` e fornecidas aos portões subsequentes.

---

## 3. Ordem Obrigatória dos Gates de Auditoria

A esteira de auditoria opera em sequência estrita e irreversível:

```text
Materializer (Sucesso)
       ↓
Execution Runtime (Comandos Executados)
       ↓
1. VALIDATION GATE (Estrutura, Sintaxe, Execução)
       ↓ (somente se PASSED)
2. QUALITY ENGINE (Testes, Linters, Dependências, Segurança)
       ↓ (somente se PASSED)
3. CERTIFICATION ENGINE (Auditoria Holística Final)
       ↓ (somente se PASSED)
PROJECT READY = YES
```

---

## 4. Gate 1: Validation Gate (`a_platform/l_validation/`)

O **ValidationGate** audita a conformidade física e estrutural básica do projeto gerado:

1. **Validação de Projeto (`ProjectValidation`):**  
   Verifica integridade do contexto, presença do plano e confirmação de materialização com status `SUCCESS`.
2. **Validação Estrutural (`StructureValidation`):**  
   - Confere se todos os arquivos listados em `expected_artifacts` existem fisicamente no disco;
   - Verifica se os arquivos contêm conteúdo não vazio (tamanho > 0 bytes);
   - Executa **compilação estática de sintaxe Python** via módulo `py_compile`, detectando erros de indentação, sintaxe ou tipagem prévia.
3. **Validação de Execução (`ExecutionValidation`):**  
   - Avalia se o status geral do `ExecutionResult` foi `PASSED`;
   - Confere se os códigos de saída foram estritamente `0`;
   - Confere a ausência de exceções não tratadas ou comandos com status `DENIED` ou `TIMEOUT`.

*Se qualquer uma das verificações falhar, o ValidationGate emite status `FAILED` com a lista detalhada de erros, acionando o ciclo de Reparo.*

---

## 5. Gate 2: Quality Engine (`a_platform/m_quality/`)

O **QualityEngine** avalia o projeto gerado através de padrões profissionais de engenharia de software e dados:

1. **Dimensão Testes (`Code Tests`):**  
   Audita a execução física do framework `pytest`. A suíte gerada pelo `TestingAgent` deve rodar com 100% dos testes aprovados. Ausência de testes em projetos analíticos acarreta nota zero nesta dimensão.
2. **Dimensão Higiene e Estilo (`Code Quality`):**  
   Execução e validação de analisadores de código (`flake8` ou `ruff`).
3. **Dimensão Segurança (`Security Quality`):**  
   Análise estática de segurança via `bandit`, bloqueando comandos inseguros, hardcoded passwords ou manipulação perigosa de strings SQL.
4. **Dimensão Dependências (`Dependency Quality`):**  
   Execução de `pip check` sobre o ambiente do projeto, garantindo consistência e ausência de conflito entre bibliotecas em `requirements.txt`.

*A aprovação requer pontuação global mínima (score >= 0.75) combinada com aprovação perfeita (1.0) nas dimensões de segurança e testes.*

---

## 6. Gate 3: Certification Engine (`a_platform/n_certification/`)

O **CertificationEngine** é a autoridade máxima e conclusiva de auditoria da fábrica:

1. **Auditoria Cruzada:** Inspeciona os laudos emitidos por todas as etapas antecedentes;
2. **Aplicação da Fórmula Estrita de Prontidão:**
   $$\text{Discovery = COMPLETE} \land \text{Planning = COMPLETE} \land \text{Materialization = SUCCESS} \land \text{Execution = PASSED} \land \text{Validation = PASSED} \land \text{Quality = PASSED}$$
3. **Emissão do Laudo Oficial:**  
   Se e somente se todas as condições forem verdadeiras, emite `CertificationResult(status="PASSED")`, autorizando a atribuição do selo `PROJECT READY = YES`.

---

## 7. Target Contract vs. Current Implementation Status

- **Target Contract:** O fluxo de gates avalia a cadeia completa de evidências reais. Qualquer inconformidade ou reprovação em Validation ou Quality interrompe o avanço e redireciona o contexto estruturado de erro para o mecanismo de diagnóstico e recuperação.
- **Current Implementation Status:** O `ValidationGate` (com subvalidações de projeto, estrutura e execução), o `QualityEngine` (com checagem de evidências físicas de testes e linters) e o `CertificationEngine` estão implementados e operam em sequência no `MasterOrchestrator`. A verificação rigorosa de saída baseada em evidência de subprocessos reais já está ativa, eliminando aprovações tácitas.

---

## Navegação

- Documento anterior: [[f_project_generation|Geração de Projetos]]
- Próximo passo funcional: [[h_repair_and_recovery|Reparo e Recuperação]]
- Referência técnica: [[i_validation_quality_certification|Validação, Qualidade e Certificação (Técnico)]]
