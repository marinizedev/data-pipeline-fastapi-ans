import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# -------------------------------
# Conexão com o MySQL
# -------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# -------------------------------
# Ler dados da staging
# -------------------------------
query = """
SELECT DISTINCT 
    reg_ans, 
    cnpj, 
    razao_social, 
    modalidade, 
    uf
FROM str_base_enriquecida
WHERE reg_ans IS NOT NULL
"""

df_operadoras = pd.read_sql(query, con=engine)

# Substituir NaN por None (garante compatibilidade com MySQL)
df_operadoras = df_operadoras.where(pd.notnull(df_operadoras), None)

# Garantir tipo correto para registro_ans
df_operadoras["reg_ans"] = df_operadoras["reg_ans"].astype(int)

# Renomear para coincidir com a tabela final
df_operadoras.columns = ["reg_ans", "cnpj", "razao_social", "modalidade", "uf"]

# Mantém apenas os 2 primeiros caracteres, ou coloca None se vazio
df_operadoras['uf'] = df_operadoras['uf'].astype(str).str[:2].replace({'': None})

print("Leitura da staging concluída!")
print("Iniciando inserção no banco...")
# -------------------------------
# Inserir na tabela final
# -------------------------------
df_operadoras.to_sql(
    "operadoras",
    con=engine,
    if_exists="append",   # append evita apagar dados já existentes
    index=False,
    chunksize=5000
)

# -------------------------------
# Verificar
# -------------------------------
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM operadoras"))
    print("Inserção concluída com sucesso!")
    print("Total de operadoras na tabela final:", result.fetchone()[0])
