# Pipeline de Ingestão de Dados

Este documento descreve as decisões técnicas adotadas na etapa de ingestão e consolidação dos dados utilizados no pipeline.

O objetivo desta etapa é garantir que os dados provenientes de fontes públicas estejam estruturados de forma consistente, permitindo processamento confiável nas fases posteriores do pipeline.

---

## Fonte dos Dados

Os dados utilizados são provenientes das Demonstrações Contábeis disponibilizadas publicamente pela ANS (Agência Nacional de Saúde Suplementar).

Foram considerados os três trimestres mais recentes disponíveis no momento da construção do projeto, referentes ao exercício de 2025.

---

## Análise Inicial da Fonte de Dados

Durante a exploração dos arquivos disponibilizados pela ANS, foi realizada uma análise inicial da estrutura dos dados, incluindo:

- identificação do formato dos arquivos
- consulta ao dicionário de dados oficial
- verificação das colunas efetivamente presentes nos arquivos trimestrais

Foi observado que alguns campos importantes para análises posteriores não estão explicitamente disponíveis nos arquivos originais.

Essa característica foi tratada como uma limitação da fonte de dados, não como erro de processamento.

---

## Decisão Técnica: Padronização Estrutural dos Dados

Para garantir consistência ao longo do pipeline, optou-se por padronizar a estrutura mínima das colunas do dataset consolidado, criando explicitamente campos necessários para etapas posteriores de validação e integração.

### Estrutura padronizada

- `regs_ans`
- `cnpj`
- `ano`
- `trimestre`
- `valor_despesas`

Campos não disponíveis na fonte original foram mantidos como valores nulos (NaN), preservando consistência estrutural do dataset.

### Justificativa

- facilita etapas posteriores de validação, enriquecimento e agregação
- evita falhas em joins decorrentes de colunas ausentes
- mantém o pipeline previsível e extensível
- garante consistência estrutural entre diferentes períodos analisados

Observação:

informações cadastrais como `razao_social`, `modalidade` e `uf` são incorporadas posteriormente na etapa de enriquecimento dos dados.

---

## Processamento dos Arquivos

Os arquivos trimestrais foram processados utilizando Python e Pandas, seguindo as etapas:

1. leitura automática dos arquivos CSV presentes em `data/raw`
2. verificação da consistência das colunas entre diferentes períodos
3. consolidação dos dados em um único dataset estruturado (DataFrame)
4. geração de arquivo CSV consolidado para uso nas etapas seguintes do pipeline

Observações:

- campos inexistentes foram preenchidos com valores nulos (NaN), garantindo consistência estrutural do dataset
- o dataset consolidado serve como base para transformações posteriores
- a estrutura padronizada facilita integração com base cadastral utilizada no enriquecimento

---

## Trade-off Técnico: Processamento em Memória

O processamento foi realizado em memória, considerando:

- volume de dados compatível com execução local
- simplicidade da arquitetura do pipeline
- facilidade de manutenção e compreensão do código

### Alternativa considerada

Uso de processamento em chunks ou persistência intermediária em banco de dados.

Essa abordagem não foi adotada por não ser necessária para o volume de dados utilizado neste projeto.

---

## Versionamento e Arquivos de Dados

Arquivos de grande volume, como CSVs consolidados e arquivos brutos, não são versionados no repositório.

Essa decisão segue boas práticas de engenharia de dados e versionamento, evitando:

- aumento desnecessário do repositório
- problemas com limites de tamanho de arquivos
- versionamento de dados derivados

Os arquivos são gerados automaticamente a partir dos scripts do projeto, garantindo reprodutibilidade completa do pipeline de ingestão.

Essa abordagem mantém o repositório focado em código e documentação, permitindo recriação dos dados sempre que necessário.