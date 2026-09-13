# Graph (Obsidian)

Embora a Fábrica tome as suas decisões através dos arquivos textuais organizados de memória no diretório `a_platform/c_brain`, a AAF suporta visualização relacional do seu conhecimento através da engine *Graph View* nativa do **Obsidian** operando no diretório root invisível `.obsidian/`.

## Relação entre Brain e Graph
- O ecossistema *Markdown* do diretório `c_brain` foi concebido abusando inteligentemente da diretiva visual `[[Link]]` típica do sistema Obsidian (ainda compatível semanticamente como referência para parsers Python/LangChain).
- O Graph provê apenas *Read-Only Awareness* ao time de Governança. Ele traduz visualmente as decisões cruzadas armazenadas sob `d_decisions` em relação às normativas de `b_rules`.
- A separação de grupos com codificação em cor (por Domínio ou Tipo de Entidade) é carregada rigidamente através do `graph.json` inserido nas *configs* da engine.

## Graph NÃO É SSOT
- **Aviso Absoluto**: O Obsidian Graph é estritamente uma **camada de visualização** passiva. O Graph NÃO rege comportamento do LLM nem controla pipeline da IDE.
- Scripts Python extraem suas intuições e padrões de regras *hard-reading* via I/O do FileSystem no `c_brain` (Single Source of Truth). O motor de dependência se baliza exclusivamente nas pastas e não nas telas, inviabilizando qualquer vício acoplado à interface visual.
