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
# Ler dados da staging despesas_consolidadas
# -------------------------------
query = """
SELECT 
    data, 
    reg_ans, 
    vl_saldo_final AS valor_despesas
FROM stg_despesas_consolidadas
WHERE reg_ans IS NOT NULL
"""

df_despesas = pd.read_sql(query, con=engine)

# Substituir NaN por None
df_despesas = df_despesas.where(pd.notnull(df_despesas), None)

# Garantir tipo correto para reg_ans
df_despesas["reg_ans"] = df_despesas["reg_ans"].astype(int)

# -------------------------------
# Extrair ano e trimestre
# -------------------------------
df_despesas["ano"] = pd.to_datetime(df_despesas["data"]).dt.year
df_despesas["trimestre"] = "T" + pd.to_datetime(df_despesas["data"]).dt.quarter.astype(str)

# -------------------------------
# Trazer o id_operadora correspondente
# -------------------------------
with engine.connect() as conn:
    # Criar um dataframe temporário com mapping reg_ans -> id_operadora
    df_operadoras = pd.read_sql("SELECT id_operadora, reg_ans FROM operadoras", con=conn)

# Merge para obter id_operadora
df_despesas = df_despesas.merge(
    df_operadoras,
    how="left",
    left_on="reg_ans",
    right_on="reg_ans"
)

# Mantém apenas colunas necessárias para tabela final
df_final = df_despesas[["id_operadora", "ano", "trimestre", "valor_despesas"]]

print("Preparação dos dados concluída!")
print("Iniciando inserção no banco...")

# Depois de fazer merge com id_operadora e extrair ano/trimestre
df_agg = df_despesas.groupby(['id_operadora', 'ano', 'trimestre'], as_index=False).agg(
    valor_despesas=('valor_despesas', 'sum')  # ou 'mean', dependendo do que a regra pede
)


# -------------------------------
# Inserir na tabela final despesas_consolidadas
# -------------------------------
df_agg.to_sql(
    "despesas_consolidadas",
    con=engine,
    if_exists="append",  # append evita apagar dados já existentes
    index=False,
    chunksize=5000
)

# -------------------------------
# Verificar
# -------------------------------
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM despesas_consolidadas"))
    print("Inserção concluída com sucesso!")
    print("Total de registros em despesas_consolidadas:", result.fetchone()[0])
