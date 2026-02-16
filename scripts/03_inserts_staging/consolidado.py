import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# Conexão com o banco (PyMySQL)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
DATABASE_URL,
echo=False,
future=True
)

# Caminho do CSV
csv_path = r"C:\Users\Marinize\Desktop\estagio-intuitivecare-dados\data\processed\02_base_consolidada_2025.csv"
print("Iniciando leitura do CSV...")

df = pd.read_csv(
    csv_path,
    sep=";", 
    encoding="latin1",
    usecols=[
    "DATA",
    "REG_ANS",
    "CD_CONTA_CONTABIL",
    "DESCRICAO",
    "VL_SALDO_INICIAL",
    "VL_SALDO_FINAL"
    ]
)

print(f"CSV lido com sucesso! Total de linhas: {len(df)}")

# DATA
df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")

# NUMÉRICOS - troca vírgula por ponto
for col in ["VL_SALDO_INICIAL", "VL_SALDO_FINAL"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",",".", regex=False)
        .astype(float)
)
    
df = df.where(pd.notnull(df), None)

# Inserção no banco (em chunks)
print("Iniciando inserção no banco...")

with engine.begin() as conn:
    df.to_sql(
        name="stg_despesas_consolidadas",
        con=conn,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
)
    
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM stg_despesas_consolidadas"))
    print(result.fetchone())

print("TOTAL NO BANCO:", result)
print("Carga concluída com sucesso!")
