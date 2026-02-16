import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

query = """
SELECT
    o.id_operadora,
    s.total_despesas,
    s.media_trimestral,
    s.desvio_padrao
FROM stg_despesas_agregadas s
JOIN operadoras o
  ON s.razao_social = o.razao_social
 AND s.uf = o.uf
"""

df_final = pd.read_sql(query, engine)

print(f"Total de registros prontos para inserção: {len(df_final)}")

df_final.to_sql(
    "despesas_agregadas",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=1000
)

print("Inserção em despesas_agregadas concluída com sucesso!")

