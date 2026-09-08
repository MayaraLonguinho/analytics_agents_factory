---
trigger: always_on
---

# IDE Agent Operational Rules (AAF)

Este documento define as regras operacionais obrigatórias para a atuação do IDE Agent no projeto **Analytics AI Factory (AAF)**. O não cumprimento destas regras resultará em quebra do fluxo canônico da fábrica.

## 1. Regras de Orquestração e Geração
- O IDE Agent atua **exclusivamente como camada de interação e orquestração**.
- O **AAF é o único responsável pela geração real dos projetos**.
- É terminantemente **proibida a geração manual de projetos** ou arquivos de código pelo Agent.
- O Agent tem a **obrigação de utilizar as interfaces oficiais do AAF** (ex: IDEAdapter).
- O Agent tem a **obrigação de reportar falhas do AAF** ao invés de tentar contorná-las gerando a funcionalidade falha manualmente.

## 2. Fluxo Obrigatório e Regra de Ouro
- O fluxo oficial deve ser rigidamente respeitado em ordem: `IDE Chat` → `IDE Adapter` → `Discovery` → `Profiling` → `Brain` → `Architecture` → `Planner` → `Factory` → `Materialization` → `Runtime` → `Validation` → `Repair` → `Quality` → `Certification`.
- A regra absoluta de **PROJECT READY**: O selo de conclusão ocorre *somente* após a passagem bem-sucedida em todas as gates obrigatórias.

## 3. Escopo e Domínio
- O escopo técnico e principal do projeto é estritamente **Analytics + Data Engineering / ETL/ELT**.
- A fábrica é **agnóstica quanto ao domínio de negócio** (Ex: finanças, ecommerce, RH são apenas contextos, não lógicas core fixadas).
- Capacidades adicionais como **dashboard, chatbot, backend e frontend são estritamente opcionais**, acionadas mediante demanda específica.
- O Agent deve garantir a **separação lógica entre contexto de negócio, project_type e domain**.
- **Não criar funcionalidades fora do escopo** solicitado pelo prompt do projeto atual.

## 4. Restrições Arquiteturais do Agent
- É **proibido implementar lógica principal do AAF dentro de `.agents`**. O núcleo funcional da fábrica reside em `a_platform`.
- É **proibido duplicar componentes existentes no núcleo do AAF** (ex: não recriar Brain, Agents, Skills, MCPs, Factory, Runtime, Validation, Quality, Certification, Learning, prompts ou workflows em `.agents`).
- **PROIBIÇÃO ABSOLUTA DE GIT**: Não executar *nenhum comando Git* neste projeto em nenhuma circunstância.
