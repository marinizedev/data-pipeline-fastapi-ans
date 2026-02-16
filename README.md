# Estágio IntuitiveCare 2026 — Projeto de Dados
Este repositório contém a solução para o **teste técnico de nivelamento** do processo seletivo de **Estágio na IntuitiveCare (2026)**.

O objetivo do projeto é demonstrar conhecimentos fundamentais em **manipulação de dados, organização de pipelines, boas práticas de desenvolvimento e capacidade analítica**, conforme as orientações fornecidas no enunciado oficial do teste.

---

## Objetivo do Projeto
Desenvolver uma solução de dados a partir de fontes públicas, contemplando etapas de **extração, tratamento, consolidação, consultas e exposição via API**, respeitando os requisitos do teste técnico proposto.

O projeto prioriza **clareza, reprodutibilidade e organização**, com documentação que justifica cada decisão técnica adotada.

---

## Contexto dos Dados
Os dados utilizados são provenientes das **Demonstrações Contábeis** disponibilizadas publicamente pela **ANS (Agência Nacional de Saúde Suplementar)**.

Observações importantes:
- Alguns campos mencionados no enunciado (como **CNPJ, razão social e despesas**) **não estão disponíveis nos arquivos originais**.
- O CNPJ encontra-se mascarado na fonte oficial; por isso, adotou-se **`registro_ans`** como identificador único confiável das operadoras.
- Foram considerados os **três trimestres mais recentes disponíveis**, referentes ao ano de **2025**.

---

## Visão Geral da Solução

A solução foi organizada em **pipeline de dados e backend**, seguindo boas práticas:

1. Leitura e extração dos arquivos trimestrais das Demonstrações Contábeis (`data/raw/`).
2. Validação da estrutura e consistência dos dados.
3. Consolidação em **CSV base** (`data/processed/02_base_consolidada_2025.csv`).
4. Transformações e enriquecimento com dados cadastrais (`04_base_enriquecida_2025.csv`).
5. Agregações analíticas (`despesas_agregadas.csv`).
6. Inserção em banco de dados relacional (**MySQL**) via scripts Python para staging e tabelas finais.
7. Implementação de API com **FastAPI** para exposição dos dados.
8. Documentação detalhada das decisões técnicas por teste (`docs/`).

---

## Tecnologias Utilizadas
- **Python** (Pandas para manipulação, scripts de inserts)
- **CSV** (entrada e saída de dados)
- **MySQL** (armazenamento relacional)
- **SQL** (consultas analíticas)
- **FastAPI** (API para exposição de dados)
- **Git / GitHub** (versionamento e entrega)

---

## Estrutura do Repositório

- /estagio-intuitivecare-dados/
- |
- |---- backend/
- |
    - |---- routers/
        - |---- despesas.py
        - |---- estatisticas.py
        - |---- operadoras.py
        - |
    - |---- database.py
    - |---- main.py
    - |---- requeriments.txt
    - |
- |---- data/
    - |---- processed/     # CSV base e CSV final
    - |---- raw/      # arquivos originais
- |
- |---- docs/
    - |---- teste_1_ingestao_e_consolidadacao.md
    - |---- teste_2_transformacao_e_validacao.md
    - |---- teste_3_sql_e_analise.md
    - |---- teste_4_interface_web.md
    - |
- |---- scripts/
    - |---- 01_extracao/
        - |---- extrair_dados.py
        - |
    - |---- 02_transform/
        - |---- agregacao_dados.py
        - |---- consolidar_dados.py
        - |---- enriquecimento_dados.py
        - |---- validacao_dados.py
        - |
    - |---- 03_inserts_staging/
        - |---- agregado.py
        - |---- consolidado.py
        - |---- enriquecido.py
        - |
    - |---- 04_inserts_oficiais
        - |---- agregado.py
        - |---- consolidado.py
        - |---- enriquecido.py
        - |
- |---- sql
    - |---- ddl_ans_despesas.sql
    - |---- ddl_queries_analytics.sql
    - |---- staging.sql
    - |
- |---- README.md

---

## Observações Técnicas Importantes

- **Arquivos grandes** (CSVs >100MB) não foram versionados; são gerados automaticamente pelos scripts.
- **__pycache__** está ignorado pelo `.gitignore`.
- Os arquivos `__init__.py` permanecem no repositório para garantir que o Python reconheça os pacotes.
- A inserção de dados no banco foi feita via **Python**, e não via `LOAD DATA INFILE`, para manter compatibilidade e segurança de execução em ambiente Windows.
- A API implementada com **FastAPI** retorna dados paginados com metadados e busca no servidor, garantindo performance mesmo com grandes volumes de dados.

---

## Adaptação do Identificador da Operadora

- Embora o enunciado mencione CNPJ, na prática **a base oficial disponibiliza o CNPJ mascarado**.
- Para consistência e integridade, **`registro_ans`** foi adotado como identificador único das operadoras, usado em todas as tabelas e relações do banco de dados.

---

## Configuração do Banco

Este projeto utiliza variável de ambiente para a string de conexão.

Defina a variável:

DATABASE_URL = mysql+pymysql://usuario:senha@localhost:3306/nome_do_banco

## Considerações Finais

Este projeto prioriza:

- Clareza e organização técnica
- Justificativa das decisões adotadas
- Qualidade e rastreabilidade dos dados
- Boas práticas em Python, SQL e desenvolvimento de APIs
- Reprodutibilidade de todo o pipeline de dados

O README reflete a **visão geral do projeto**, enquanto os detalhes técnicos de cada teste estão documentados separadamente em `docs/`.

---

## Autora

**Marinize Santana** – desenvolvimento da solução como parte do teste técnico de nivelamento do processo seletivo de **Estágio na IntuitiveCare (2026)**.
