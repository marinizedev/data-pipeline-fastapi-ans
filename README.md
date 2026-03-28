![Python](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)

# Pipeline de Dados e API REST com FastAPI
Este projeto implementa um pipeline completo de dados, contemplando extração, validação, transformação, consolidação e disponibilização de informações por meio de uma API REST desenvolvida com FastAPI.

A solução foi construída com foco em organização, reprodutibilidade e clareza arquitetural, aplicando boas práticas de engenharia de dados e desenvolvimento backend.

O pipeline processa dados públicos da ANS (Agência Nacional de Saúde Suplementar), realizando preparação analítica e exposição estruturada dos dados para consumo por aplicações externas.

---

## Objetivo do Projeto
Demonstrar a construção de um fluxo de dados estruturado a partir de fontes públicas, incluindo:

- ingestão de dados
- validação de consistência
- transformação e padronização
- enriquecimento com dados cadastrais
- agregações analíticas
- persistência em banco relacional
- disponibilização via API REST

O projeto prioriza:

- organização de pipeline
- rastreabilidade dos dados
- separação de responsabilidades
- clareza na modelagem relacional
- reprodutibilidade do ambiente

---

## Contexto dos Dados
Os dados utilizados são provenientes das Demonstrações Contábeis disponibilizadas publicamente pela ANS (Agência Nacional de Saúde Suplementar).

Observações relevantes:
- Alguns campos presentes em bases públicas possuem limitações de disponibilidade.
- O CNPJ encontra-se mascarado na fonte oficial; por isso, adotou-se `registro_ans` como identificador único confiável das operadoras.
- Foram considerados os três trimestres mais recentes disponíveis referentes ao ano de 2025.
- Os dados são tratados e organizados para permitir análises comparativas e consultas estruturadas.

---

## Arquitetura da Solução
Fluxo simplificado do pipeline:

```bash
Fonte de dados (ANS)
        ↓
Extração (Python)
        ↓
Validação e padronização
        ↓
Transformação (Pandas)
        ↓
Enriquecimento e agregações
        ↓
Persistência relacional (MySQL)
        ↓
API REST (FastAPI)
```

---

## Tecnologias Utilizadas
- **Python**
- **Pandas**
- **SQL** 
- **MySQL**
- **FastAPI**
- **CSV** 
- **Git e GitHub**

---

## Estrutura do Repositório

```bash
data-pipeline-fastapi-ans/
│
├── backend/
│   ├── routers/
│   │   ├── despesas.py
│   │   ├── estatisticas.py
│   │   └── operadoras.py
│   ├── database.py
│   ├── main.py
│   └── requirements.txt
│
├── data/
│   ├── processed/
│   └── raw/
│
├── docs/
│   ├── pipeline_ingestao.md
│   ├── pipeline_transformacao.md
│   ├── analise_sql.md
│   └── api_interface.md
│
├── scripts/
│   ├── 01_extracao/
│   ├── 02_transform/
│   ├── 03_inserts_staging/
│   └── 04_inserts_oficiais/
│
├── sql/
└── README.md
```

---

## Observações Técnicas Importantes

- **Arquivos grandes** (CSVs >100MB) não foram versionados; são gerados automaticamente pelos scripts.
- **__pycache__** está ignorado pelo `.gitignore`.
- Os arquivos `__init__.py` permanecem no repositório para garantir que o Python reconheça os pacotes.
- A inserção de dados no banco foi feita via **Python**, e não via `LOAD DATA INFILE`, para manter compatibilidade e segurança de execução em ambiente Windows.
- A API implementada com **FastAPI** retorna dados paginados com metadados e busca no servidor, garantindo performance mesmo com grandes volumes de dados.

---

## Configuração do Banco

Este projeto utiliza variável de ambiente para a string de conexão.

```bash
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/nome_do_banco
```

## Como Reproduzir o Projeto

### Clonar o repositório

```bash
git clone https://github.com/marinizedev/data-pipeline-fastapi-ans.git
cd data-pipeline-fastapi-ans
```

### Criar ambiente virtual

```bash
python -m venv venv
```

Ativar:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Configurar variável de ambiente

No Windows (PowerShell):

```bash
setx DATABASE_URL "mysql+pymysql://usuario:senha@localhost:3306/nome_do_banco"
```

No Linux/Mac:

```bash
export DATABASE_URL="mysql+pymysql://usuario:senha@localhost:3306/nome_do_banco"
```

### Executar pipeline

Executar scripts na seguinte ordem:

```bash
python scripts/01_extracao/extrair_dados.py
python scripts/02_transform/consolidar_dados.py
python scripts/02_transform/validacao_dados.py
python scripts/02_transform/enriquecimento_dados.py
python scripts/02_transform/agregacao_dados.py
```

### Inserir dados no banco

Executar os scripts das pastas `03_inserts_staging/` e `04_inserts_oficiais/`.

### Subir a API

```bash
uvicorn backend.main:app --reload
```

Acessar:

API:

http://127.0.0.1:8000

Documentação automática:

http://127.0.0.1:8000/docs

### Exemplos de Endpoints

- `GET /operadoras`
- `GET /despesas`
- `GET /estatisticas`

Mini exemplo:

```json
{
  "total": 120,
  "pagina": 1,
  "dados": [
    {
      "registro_ans": "12345",
      "despesa_total": 987654.32
    }
  ]
}
```

---

## Desenvolvido por:

**Marinize Santana** – Projeto desenvolvido para fins de estudo e prática em engenharia de dados, com foco em construção de pipelines reprodutíveis e APIs de dados.
