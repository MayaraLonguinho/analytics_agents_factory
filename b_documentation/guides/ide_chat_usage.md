# Guia de Uso: IDE Chat (Interface Principal)

O IDE Chat é a interface nativa e primária do Analytics AI Factory, operando através do `IDEAdapter`. A plataforma atua como uma engine embedded, interagindo diretamente com o usuário no ambiente de desenvolvimento.

## Como preparar a IDE
Abra a pasta raiz do projeto (`analytics_agents_factory`) em sua IDE preferida (Cursor, VS Code com Claude Dev / Cline, ou Devin). Certifique-se de que o agente (extensão) tenha visibilidade total do workspace.

## Configuração de Chaves
As chaves de API devem estar configuradas no arquivo `.env` na raiz do projeto, ou configuradas diretamente nas extensões da IDE correspondente, dependendo da sua escolha.

## Como Iniciar a Interação
No chat da IDE, inicie uma interação com um prompt claro, como por exemplo:
> "Crie um projeto de Analytics que leia um dataset CSV, faça limpeza de dados e gere um relatório de vendas."

## Ciclo de Discovery Interativo
O motor iniciará a etapa de Discovery. Se houver ambiguidades, o motor entrará em estado `NEEDS_INPUT`.
- **Exemplo de pergunta do motor:** "Qual deve ser o separador do arquivo CSV? Existem colunas de datas específicas que devem ser convertidas?"
- **Exemplo de resposta:** "O separador é vírgula. A coluna 'data_venda' deve ser convertida para datetime."

## Acompanhamento e Sucesso
O progresso pode ser acompanhado diretamente no chat. Os artefatos finais serão materializados em:
`e_generated_projects/<domain>/<project_id>/`

Você deve inspecionar os logs de execução para confirmar o status final como:
`PROJECT READY = YES`

## Tratamento de Falhas
Caso alguma validação falhe e o status retorne `PROJECT READY = NO`, o Repair Loop entrará em ação automaticamente para tentar corrigir o código (até 3 tentativas). Se a falha persistir, você pode verificar os logs em `.aaf_state/` ou na própria IDE e fornecer feedback no chat para correção.
