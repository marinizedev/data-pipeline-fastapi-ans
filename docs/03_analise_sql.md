# Análise de Dados em SQL

Este documento descreve as decisões técnicas relacionadas à **modelagem do banco de dados**, estratégia de carga dos dados e construção de **queries analíticas** a partir dos datasets gerados nas etapas anteriores do pipeline.

O objetivo foi estruturar os dados de forma consistente, garantindo integridade referencial e suporte a análise estatísticas. 

---

## Arquivos Utilizados

Para criação das tabelas e execução das análises, foram utilizados os seguintes arquivos CSV gerados no pipeline:

- **02_base_consolidada_2025.csv**
Dataset contendo despesas consolidadas por operadora, trimestre e ano.  
- **04_base_enriquecida_2025.csv** 
Dataset resultante do enriquecimento da base consolidada com dados cadastrais das operadoras (registro ANS, modalidade e UF).  
- **despesas_agregadas.csv**
Dataset contendo métricas estatísticas por operadora e unidade federativa, incluindo soma total, média e desvio padrão das despesas.  

Esses arquivos representam diferentes níveis do pipeline:
- dado consolidado
- dado enriquecido
- dado agregado

Permitindo análises detalhadas e visões resumidas.

---

## Estratégia de Modelagem

### Abordagem adotada: modelo normalizado

A modelagem foi estruturada com separação lógica entre:

- dados cadastrais das operadoras  
- dados consolidados de despesas  
- dados agregados para análise  

### Justificativa

- evita duplicação de informações cadastrais
- melhora a integridade dos dados
- facilita manutenção
- permite consultas analíticas eficientes
- mantém rastreabilidade das transformações do pipeline

Dados cadastrais possuem menor frequência de atualização, enquanto despesas são atualizadas periodicamente, justificando a separação em tabelas distintas.

---

## Estrutura das Tabelas

### Tabela `operadoras`

Armazena informações cadastrais das operadoras de planos de saúde.  

Campos:

- `id_operadora` (chave primária)
- `reg_ans`
- `cnpj`
- `razao_social`
- `modalidade`
- `uf`

Índices:

- índice em `uf`para otimizar consultas por estado

---

### Tabela `despesas_consolidadas`

Armazena valores de despesas por operadora período.

Campos:

- `id` (chave primária técnica)
- `id_operadora` (chave estrangeira) 
- `ano`  
- `trimestre`  
- `valor_despesas`  

Restrições:

- chave estrangeira → `operadoras`(`id_operadora`)
- UNIQUE (`id_operadora`, `ano`, `trimestre`)

Justificativa do UNIQUE: 

Garante que uma operadora não possua registros duplicados no mesmo período.

Índices:

- índices em `ano`
- índice em `trimestre`

---

### Tabela `despesas_agregadas`

Armazena métricas estatísticas derivadas das despesas.  

Campos:

- `id` (chave primária técnica) 
- `id_operadora` (chave estrangeira) 
- `total_despesas`  
- `media_trimestral`  
- `desvio_padrao`  

Índices:

- índices em `id_operadora`

Observação:

Os nomes das colunas seguem padrão `snake_case`, mantendo consistência com a modelagem relacional e facilitando integração com queries SQL.

---

## Trade-off Técnico — Tipos de Dados

Escolha dos tipos de dados:

- valores monetários → `DECIMAL(15,2)`
- ano → `INT`
- trimestre → `VARCHAR`
- identificadores → `INT`

Justificativa:

- DECIMAL evita imprecisão comum em FLOAT
- tipos simples facilitam integração com Python e Pandas
- compatibilidade com estrutura dos CSVs originais
- precisão adequada para valores financeiros

---

## Abordagem em Camadas

Foi adotada uma estrutura em duas camadas:

### Camada de staging

Mantém estrutura próxima aos arquivos CSV originais.

Objetivos:
- facilitar ingestão
- evitas perda de informação
- permitir rastreabilidade de inconsistências
- garantir compatibilidade com diferentes formatos de entrada

### Camada analítica normalizada

Estrutura otimizada para:
- integridade referencial
- performance
- clareza nas consultas 
- facilidade de manutenção

Essa separação melhora a organização do pipeline e facilita evolução futura do projeto.

---

### Estratégia de Carga de Dados

A inserção dos dados foi realizada utilizando Python, permitindo:
- controle de tipos de dados
- tratamento de valores nulos
- inserção em lote
- rastreabilidade com ambiente local

Essa abordagem evita dependência de configurações específicas do banco de dados e mantém consistência com as etapas anteriores do pipeline.

---

## Queries Analíticas em SQL

As análises foram realizadas utilizando as tabelas:

- operadoras
- despesas_consolidadas
- despesas_agregadas

---

### Query 1 — Crescimento percentual de despesas por operadora

Objetivo: 

Identificar operadoras com maior variação percentual de despesas entre períodos analisados.  

Estratégia:

- comparação entre valores de períodos distintos
- cálculo de crescimento percentual
- tratamento de valores nulos
- prevenção de divisão por zero

Essa análise permite identificar tendências de crescimento ou redução de custos ao longo do tempo.

---

### Query 2 — Distribuição de despesas por UF

Objetivo: 

Analisar concentração de despesas por unidade federativa.

Estratégia:
- soma total das despesas por UF
- cálculo de média por operadora
- ordenação decrescente

Permite identificar regiões com maior volume financeiro.

---

### Query 3 — Operadoras com despesas acima da média

Objetivo: 

Identificar operadoras com desempenho acima da média em múltiplos períodos.

Estratégia:

- cálculo da média geral
- comparação por período
- uso de CTEs para melhorar legibilidade
- contagem de ocorrências acima da média

Essa abordagem facilita manutenção e interpretação da query.

---

## Observações Técnicas

A estrutura do banco foi projetada considerando:

- clareza da modelagem 
- integridade dos dados
- facilidade de manutenção
- compatibilidade com ferramentas de análise
- possibilidade de expansão futura do pipeline

O uso combinado de Python, Pandas e SQL permitiu construir um fluxo consistente de preparação e análise de dados.
