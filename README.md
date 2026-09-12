# Analytics Agents Factory (AAF)

## Objetivo
Uma fábrica de software totalmente gerida por agentes autônomos, focada em engenharia de dados e analytics. A AAF atua em todo o ciclo de vida do projeto: discovery, planning, arquitetura, codificação, validação, qualidade e certificação. Não utiliza templates fixos ou caminhos engessados.

## Funcionamento
O sistema opera através de um hub de especialidades (Agents) operados por um `MasterOrchestrator`. A lógica operacional é **100% autônoma**, guiada por capabilities e domains. O `Brain` atua como fonte de verdade de conhecimento e padrões, ditando restrições de arquitetura e contexto, substituindo o uso de documentação extensa (Markdown) em favor de operações compactas (Context Packs).

## Como Executar

Para iniciar a experiência completa e solicitar a criação de um projeto:
```bash
python aaf start
```
*(Durante a execução, o agente de discovery fará o alinhamento antes do planejamento e execução).*

Para rodar demonstrações de Model Context Protocols (MCPs):
```bash
python aaf mcp
```

## Arquitetura
A AAF possui um design pautado em camadas rigorosas (Gates):
- **Core / Brain**: Registros de conhecimento, regras de negócio e limites de memória (Context Pack).
- **Agents & Skills**: Entidades isoladas com ferramentas focadas (ex: DiscoveryAgent, PlannerAgent).
- **Factory & Materializer**: Foca em produzir e injetar o plano físico.
- **Validation, Quality, Certification**: Tripla checagem onde um projeto só sobrevive se o código real executar (Exit Code 0), tiver testes passando e atingir patamar mínimo de qualidade estrutural e de dependências.

## Demo
O funcionamento básico e as integrações são demonstradas via `aaf start` e também pelo script sintético de validação dos portões:
```bash
python test_synthetic_gates.py
```
*(Demonstra o ciclo de sucesso ou reparo - Repair Loop - a partir de uma quebra no meio da execução).*
