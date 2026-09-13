# Roteiro de Demonstração (Presentation)

Siga os passos a seguir para provar a plena sanidade operacional e as barreiras conceituais (agentes, qualidade rígida, MCP local) da **Analytics Agents Factory** (AAF) aos *stakeholders*.

## Execução Prática

1. **Invocação Básica**
Abra o console na raiz e chame a porta de entrada via CLI com um requisito simples para gerar carga.
```bash
python -m a_platform.b_interfaces.b_cli.c_commands start --prompt "Criar script de ingestão Python conectando a uma API JSON de moedas e salvando em SQLite" --dataset "./d_input/sample.csv"
```

2. **Demonstrar Brain & Graph**
Abra a raiz de projeto no programa *Obsidian* ou aponte os logs gerados durante as deliberações do *ArchitectureAgent*. O log evidenciará o agente lendo `c_brain/b_rules/` em vez de decidir aleatoriamente. Demonstre ao vivo que a factory adota a regra em código real.

3. **Geração via Factory e Sandbox MCP**
Mostre a orquestração gerando código estruturado na pasta segura `e_generated_projects/`. Comente a imunidade de invasões do *Filesystem MCP* a qualquer gravação fora da hierarquia permitida. Mostre os `Agents` delegando LLM calls no *Gateway*.

4. **Runtime & Validação (Execução e Testes)**
Conforme o *CLI status* atualiza, acompanhe o `j_runtime` disparar o pacote instanciado contra o `Docker MCP`.

5. **Certification & PROJECT READY**
Mostre os _logs_ onde o `ValidationGate` passa, avançando à `QualityEngine`. Explicite como o `tests_ok` e os `scores` de `m_certification` extraíram os *Assets* provando testes no script alvo. Ao final, a saída dourada:

```
===============================================
🏆 PROJECT READY = YES (proj-xxx)
===============================================
```

Estará pronta para ser consumida validada, livre de suposições ou aprovações fantasmas baseadas em falso silêncio (mock).
