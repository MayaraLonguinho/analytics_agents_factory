# Validation Gate

A camada `k_validation` instaura o veredito primário se os processos executados pela máquina `j_runtime` não quebraram durante o disparo inicial.

## Validation Gate e Critérios de Aceitação
- Uma execução pode simplesmente declarar `SUCCESS` internamente ao não explodir, mas se o script subjacente gerar saídas indesejáveis (análises sintáticas defeituosas em logs Python ou Erros T-SQL silenciosos), o `a_validation_gate.py` detecta.
- Avalia **evidências fidedignas** recuperando as assinaturas dos relatórios da fase passada (a `last_execution_result`).
- Apenas execuções contendo explicitamente o status `SUCCESS` contam como provadas. O flag default `passed: True` gerado passivamente foi banido. Sem artefatos e log palpável, `passed` assume `False`.

## Ciclos de Reparo (Repair Loop)
Se o `ValidationGate` travar o progresso reprovando a fase, a estrutura orquestradora (em `n_orchestration`) suspende temporariamente o avanço à Qualidade e aciona a `ProjectPhase.REPAIR_LOOP`.
- Este Repair Loop avalia os metadados de reprovação.
- Uma nova tarefa intercede para remendar sintaxe falha/dependência não encontrada sem descartar a fundação original do projeto.
- Isso corre até 3 vezes (`max_repair_attempts`).
- Uma segunda rejeição total no pipeline esgotará as tentativas falhando o projeto (`FAILED`) e devolvendo um reporte definitivo ao cliente da Factory.
