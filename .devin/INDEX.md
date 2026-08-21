# Integração Devin

## Objetivo

O diretório `.devin/` contém exclusivamente os componentes necessários para integrar o Devin ao Analytics AI Factory.

## Responsabilidade

O Devin atua como uma camada de integração.

A lógica principal do AAF não deve ser implementada neste diretório.

## Estrutura

```text
.devin/
├── AGENT.md
├── AGENTS.md
├── INDEX.md
├── config.local.json
├── a_agents/
├── b_prompts/
├── c_rules/
├── d_skills/
├── e_workflows/
├── f_memories/
├── g_settings/
└── h_context/

# Índice do Adaptador Devin

O Devin é uma camada de integração do Analytics AI Factory.

O diretório `.devin/` não contém a lógica principal do AAF.

O núcleo do Analytics AI Factory é responsável por:

- entrada;
- descoberta;
- profiling de datasets;
- Brain;
- planejamento;
- agentes;
- skills;
- MCP;
- LLM Gateway;
- Factory;
- materialização;
- runtime;
- validação;
- qualidade;
- certificação;
- aprendizado.

## Componentes do Adaptador Devin

- `AGENT.md` — instruções principais da integração com o Devin.
- `AGENTS.md` — instruções do adaptador de repositório.
- `a_agents/` — configuração de integração dos agentes com o Devin.
- `b_prompts/` — prompts utilizados para reconhecimento e encaminhamento de comandos.
- `c_rules/` — regras específicas da integração com o Devin.
- `d_skills/` — skills específicas da integração com o Devin.
- `e_workflows/` — workflows utilizados pela integração.
- `f_memories/` — configuração da integração de memória.
- `g_settings/` — configurações específicas do ambiente Devin.
- `h_context/` — configuração de contexto da integração.

## Independência do Núcleo

O Analytics AI Factory deve funcionar sem depender do Devin.

O Devin somente fornece uma camada de integração sobre as interfaces do AAF.

Nenhuma lógica principal do produto deve depender de arquivos localizados em `.devin/`.

## Domínios da Primeira Versão

A primeira versão do Analytics AI Factory possui foco em:

- Analytics;
- Data Engineering.

Outros domínios poderão ser adicionados futuramente pelo núcleo do AAF sem exigir alterações estruturais no adaptador Devin.

## Projetos Gerados

Projetos gerados pelo AAF devem permanecer fora de `.devin/`.

A localização oficial dos projetos gerados será:

`p_output/a_projects/`

O adaptador Devin não deve criar diretamente os arquivos dos projetos gerados.