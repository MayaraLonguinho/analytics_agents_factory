# Ciclo de Vida do Conhecimento

## Objetivo

Este documento descreve o ciclo de vida do conhecimento no Brain, desde sua criação até sua eventual remoção ou arquivamento. Cada tipo de conhecimento (Internal, External, Generated) tem seu próprio ciclo de vida.

## Ciclo de Vida do Internal Knowledge

### Criação

O Internal Knowledge é criado durante o desenvolvimento do projeto:

1. **Arquitetura**: Criada durante o design inicial do sistema
2. **ADRs**: Criados quando decisões arquiteturais são tomadas
3. **Padrões**: Documentados quando padrões são estabelecidos
4. **Regras**: Definidas quando convenções são estabelecidas
5. **Exemplos**: Criados quando componentes são implementados
6. **Personal Finance Flow**: Populado gradualmente com conhecimento do projeto de referência

### Registro

Após criação, o conhecimento é registrado no Knowledge Registry:

```python
# Registro de nova fonte
registry.register(
    id="new-pattern-001",
    type="internal",
    category="patterns",
    path="internal_knowledge/patterns/new_pattern.md",
    metadata={
        "name": "New Pattern",
        "description": "Novo padrão documentado",
        "version": "1.0",
        "created_at": datetime.utcnow().isoformat()
    }
)
```

### Atualização

O Internal Knowledge é atualizado quando:

- Novos padrões são adotados
- Decisões arquiteturais mudam (novos ADRs)
- Convenções são atualizadas
- Exemplos são adicionados ou melhorados
- Personal Finance Flow evolui

**Processo de Atualização**:
1. Modificar o conhecimento
2. Atualizar versão nos metadados
3. Atualizar timestamp
4. Notificar Agents sobre mudanças
5. Manter histórico se necessário

### Versão

O Internal Knowledge é versionado com o projeto:

- **Maior Versão**: Mudanças significativas que quebram compatibilidade
- **Menor Versão**: Novas funcionalidades, compatibilidade mantida
- **Patch**: Correções de bugs, compatibilidade mantida

### Arquivamento

Conhecimento antigo pode ser arquivado quando:

- Padrões são substituídos por novos
- Tecnologias são descontinuadas
- Projetos de referência são atualizados
- Conhecimento torna-se obsoleto

**Processo de Arquivamento**:
1. Marcar como arquivado nos metadados
2. Mover para diretório de arquivamento
3. Manter disponível para referência histórica
4. Não remover do Knowledge Registry

## Ciclo de Vida do External Knowledge

### Descoberta

O External Knowledge é descoberto quando:

- Novas bibliotecas são adotadas
- Novos frameworks são integrados
- Novos padrões da indústria são identificados
- Novos recursos da comunidade são encontrados

### Registro

Após descoberta, o conhecimento é registrado:

```python
# Registro de fonte externa
registry.register(
    id="anthropic-docs-001",
    type="external",
    category="anthropic",
    path="external_knowledge/anthropic/",
    metadata={
        "name": "Anthropic Documentation",
        "description": "Documentação oficial da Anthropic",
        "version": "2024.01",
        "url": "https://docs.anthropic.com",
        "last_checked": datetime.utcnow().isoformat()
    }
)
```

### Verificação

O External Knowledge é verificado periodicamente:

- **Frequência**: Mensal ou trimestral
- **Verificações**:
  - Links ainda estão válidos
  - Documentação foi atualizada
  - Versões mudaram
  - Novos recursos foram adicionados

### Atualização

O External Knowledge é atualizado quando:

- Documentação oficial é atualizada
- Novas versões de bibliotecas são lançadas
- Novos padrões são estabelecidos
- Links mudam ou são descontinuados

**Processo de Atualização**:
1. Detectar mudança (manual ou automático)
2. Atualizar conteúdo se necessário
3. Atualizar metadados (versão, timestamp)
4. Notificar Agents sobre mudanças

### Remoção

O External Knowledge é removido quando:

- Bibliotecas são descontinuadas
- Links tornam-se permanentemente inválidos
- Conhecimento não é mais relevante
- Projetos de referência são removidos

**Processo de Remoção**:
1. Marcar como obsoleto nos metadados
2. Notificar Agents sobre remoção
3. Aguardar período de grace
4. Remover do Knowledge Registry

## Ciclo de Vida do Generated Knowledge

### Geração

O Generated Knowledge é criado automaticamente pelos Agents:

- **Reports**: Gerados após execução de workflows
- **Analyses**: Gerados pelo Analytics Agent
- **Plans**: Gerados pelo Planner Agent
- **Decisions**: Registrados quando Agents tomam decisões
- **Metrics**: Calculados durante execução
- **Summaries**: Gerados ao processar dados
- **Insights**: Descobertos durante análises
- **Recommendations**: Produzidos por Agents

### Registro

Após geração, o conhecimento é registrado:

```python
# Registro de conhecimento gerado
registry.register(
    id="generated-analysis-001",
    type="generated",
    category="analyses",
    path="generated_knowledge/analyses/analysis_001.json",
    metadata={
        "name": "Analysis 001",
        "description": "Análise gerada automaticamente",
        "generated_by": "analytics_agent",
        "generated_at": datetime.utcnow().isoformat(),
        "context": {"project": "project_a", "data": "sales"}
    }
)
```

### Retenção

O Generated Knowledge segue políticas de retenção:

- **Reports**: 90 dias
- **Analyses**: 180 dias
- **Plans**: 365 dias
- **Decisions**: 365 dias
- **Metrics**: 180 dias
- **Summaries**: 90 dias
- **Insights**: 365 dias
- **Recommendations**: 180 dias

**Política de Retenção**:
```python
retention_policies = {
    "reports": 90,
    "analyses": 180,
    "plans": 365,
    "decisions": 365,
    "metrics": 180,
    "summaries": 90,
    "insights": 365,
    "recommendations": 180
}
```

### Arquivamento

Quando o período de retenção expira, o conhecimento é arquivado:

**Processo de Arquivamento**:
1. Verificar idade do conhecimento
2. Avaliar relevância (popularidade, acessos recentes)
3. Se irrelevante, mover para arquivamento
4. Se relevante, estender retenção
5. Comprimir se apropriado

### Limpeza

O Generated Knowledge é limpo periodicamente:

- **Frequência**: Semanal
- **Processo**:
  1. Identificar conhecimento expirado
  2. Avaliar se deve ser arquivado ou removido
  3. Arquivar se potencialmente útil
  4. Remover se definitivamente obsoleto
  5. Atualizar Knowledge Registry

## Estatísticas de Conhecimento

O Knowledge Registry mantém estatísticas:

```python
knowledge_stats = {
    "internal": {
        "total": 50,
        "by_category": {
            "architecture": 10,
            "patterns": 15,
            "rules": 10,
            "examples": 15
        }
    },
    "external": {
        "total": 30,
        "by_category": {
            "anthropic": 5,
            "documentation": 15,
            "github_examples": 10
        }
    },
    "generated": {
        "total": 1000,
        "by_category": {
            "reports": 200,
            "analyses": 300,
            "plans": 100,
            "decisions": 400
        }
    }
}
```

## Monitoramento

O ciclo de vida do conhecimento é monitorado:

### Alertas

- **Conhecimento Expirado**: Quando período de retenção expira
- **Links Quebrados**: Quando external knowledge tem links inválidos
- **Baixa Utilização**: Quando conhecimento não é acessado por período longo
- **Alta Utilização**: Quando conhecimento é muito utilizado (candidato a cache)

### Métricas

- **Taxa de Criação**: Novo conhecimento criado por período
- **Taxa de Atualização**: Conhecimento atualizado por período
- **Taxa de Remoção**: Conhecimento removido por período
- **Taxa de Acesso**: Acessos por período
- **Tempo de Vida Médio**: Idade média do conhecimento

## Backup

O conhecimento é backupado regularmente:

- **Internal Knowledge**: Backup diário, versionado com git
- **External Knowledge**: Backup semanal, referências a recursos externos
- **Generated Knowledge**: Backup diário, política de retenção aplicada

## Recuperação

Em caso de perda, o conhecimento pode ser recuperado:

- **Internal Knowledge**: Recuperado do git
- **External Knowledge**: Recuperado de backup ou re-descoberto
- **Generated Knowledge**: Recuperado de backup (se ainda na janela de retenção)

## Manutenção

### Rotina de Manutenção

**Diária**:
- Verificar novos conhecimentos gerados
- Aplicar políticas de retenção
- Limpar conhecimento expirado

**Semanal**:
- Verificar external knowledge (links, atualizações)
- Atualizar estatísticas
- Revisar alertas

**Mensal**:
- Revisar políticas de retenção
- Arquivar conhecimento antigo
- Atualizar documentação

**Trimestral**:
- Revisar ciclo de vida do conhecimento
- Ajustar políticas se necessário
- Relatório de métricas

## Melhoria Contínua

O ciclo de vida do conhecimento é melhorado continuamente:

- **Feedback**: Coletar feedback dos Agents sobre utilidade do conhecimento
- **Análise**: Analisar padrões de acesso e utilização
- **Otimização**: Otimizar políticas baseadas em análise
- **Evolução**: Evoluir o sistema conforme necessário

## Nota Importante

**O ciclo de vida do conhecimento não depende de RAG, busca semântica ou banco vetorial.** Ele é gerenciado de forma determinística baseada em políticas, metadados e tempo. A classificação e organização do conhecimento é feita manualmente ou automaticamente baseada em regras claras, não em aprendizado de máquina ou similaridade semântica.
