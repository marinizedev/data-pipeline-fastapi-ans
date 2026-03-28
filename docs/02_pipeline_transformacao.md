# Pipeline de Transformação de Dados

Este documento descreve as decisões técnicas adotadas nas etapas de **validação, enriquecimento e agregação de dados** do pipeline.

O objetivo desta etapa foi garantir consistência mínima da base e gerar um dataset analítico estruturado para uso em análises e consultas posteriores.

---

## Validação de Dados

A partir do dataset consolidado gerado na etapa de ingestão (`02_base_consolidada_2025.csv`), foi implementada uma etapa de validação com o objetivo de identificar inconsistências estruturais antes do enriquecimento e da agregação.

As validações foram aplicadas considerando os campos disponíveis nesse estágio do pipeline.

Foram aplicadas as seguintes verificações:

### CNPJ
- Validação de formato
- Cálculo dos dígitos verificadores
- Identificação de registros inválidos

### REGS_ANS
- verificação de valores nulos
- verificação de formato inválido

### Valor de Despesas
- Conversão para tipo numérico
- Identificação de valores negativos
- tratamento de valores não numéricos

### Estratégia para Dados inválidos (Trade-off técnico)

Registros inconsistentes **não foram removidos** da base.

Em vez disso, foram criadas **flags de validação**, permitindo:

- preservação da rastreabilidade dos dados
- auditoria futura
- reprocessamento posterior
- transparência sobre a qualidade de base

Essa abordagem mantém o pipeline resiliente e evita perda de informação potencialmente relevante.

---

## Enriquecimento dos Dados

### Objetivo

Complementar a base consolidada de despesas com informações cadastrais das operadoras de planos de saúde.

### Bases utilizadas

- Base consolidada de despesas `02_base_consolidada_2025.csv`
- Cadastro de operadoras ativas `operadoras_ativas.csv`

### Desafio encontrado

As bases utilizam nomes diferentes para a coluna de chave utilizada no relacionamento:

```bash
| Base     | Coluna             |
| -------- | ------------------ |
| Despesas | REG_ANS            |
| Cadastro | REGISTRO_OPERADORA |
```

Foi necessário realizar padronização prévia para permitir a correspondência correta dos registros.

### Estratégia adotada

- leitura dos arquivos com separador correto (`;`)
- uso de encoding `latin1`
- conversão das colunas-chave para tipo string
- remoção de espaços em branco
- seleção apenas das colunas necessárias do cadastro
- remoção de duplicidades
- aplicação de LEFT JOIN

O uso de LEFT JOIN garante que todos os registros da base de despesas sejam preservados, mesmo quando não existe correspondência no cadastro.

### Resultado

Inclusão das seguintes colunas provenientes do cadastro:

- Razao_Social
- Modalidade
- UF

Arquivo gerado:

`04_base_enriquecida_2025.csv`

---

## Agregação dos Dados

### Objetivo

Gerar um dataset analítico contendo métricas estatísticas de despesas por operadora e unidade federativa.

### Base utilizada

Base enriquecida com dados cadastrais das operadoras:

`04_base_enriquecida_2025.csv`

### Variáveis utilizadas na agregação

O processo de agregação utiliza os nomes das colunas conforme presentes no dataset enriquecido:

- Razao_Social
- UF
- ValorDespesas

### Métricas calculadas

Para cada combinação de:
- Razao_Social
- UF

Foram calculados:
- soma total das despesas (`sum`)
- média trimestral das despesas (`mean`)
- desvio padrão das despesas (`std`)

### Problema identificado

Durante a execução inicial, o dataset agregado foi gerado vazio.

A análise identificou inconsistência no nome da coluna utilizada na agregação:

RazaoSocial ≠ Razao_Social

Diferença de nomenclatura entre colunas impedia a correspondência correta durante o agrupamento (`groupby`), resultando em um DataFrame vazio.

### Correções aplicadas

- padronização dos nomes das colunas
- conversão explícita da coluna `ValorDespesas` para tipo numérico
- remoção de espaços em branco nas colunas categóricas
- inclusão de verificações intermediárias para validação do volume de dados antes da agregação

### Resultado final

O processo de agregação foi executado com sucesso, gerando o arquivo:

`despesas_agregadas.csv`

Casos com apenas um trimestre apresentaram valor nulo de desvio padrão, comportamento esperado estatisticamente. Esses valores foram posteriormente tratados para manter consistência do dataset final.

---

## Observações Técnicas

Durante o desenvolvimento, foram identificadas diferenças entre a expectativa estrutural do dataset e os dados efetivamente disponíveis.

O pipeline foi desenvolvido priorizando:
- reprodutibilidade
- clareza do código
- rastreabilidade dos dados
- robustez contra inconsistências da fonte
- separação de responsabilidades entre etapas do pipeline