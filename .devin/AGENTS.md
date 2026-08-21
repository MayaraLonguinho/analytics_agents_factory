# Adaptador de repositório Devin

Utilize os componentes canônicos listados em `INDEX.md`.

Este diretório pertence exclusivamente à integração do Analytics AI Factory com o Devin.

O Devin deve utilizar as interfaces e componentes fornecidos pelo núcleo do AAF.

Não implemente neste diretório:

- Brain;
- Planning;
- Factory;
- Materialization;
- Runtime;
- Validation;
- Quality;
- Certification;
- Learning.

Essas responsabilidades pertencem ao núcleo do Analytics AI Factory.

Quando uma funcionalidade necessária ainda não existir no núcleo do AAF, ela deve ser criada no núcleo correspondente, e não dentro de `.devin/`.

O adaptador Devin deve permanecer substituível e não pode ser uma dependência obrigatória do Analytics AI Factory.