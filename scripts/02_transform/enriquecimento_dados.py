import pandas as pd
from pathlib import Path

# -------------------------------
# Caminhos
# -------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR / "data" / "raw"

input_file = PROCESSED_DIR / "02_base_consolidada_2025.csv"
cadastro_file = RAW_DIR / "operadoras_ativas.csv"
output_file = PROCESSED_DIR / "04_base_enriquecida_2025.csv"

# -------------------------------
# Leitura dos CSVs
# -------------------------------
df_despesas = pd.read_csv(input_file, sep=";", encoding="latin1")
df_cadastro = pd.read_csv(cadastro_file, sep=";", encoding="latin1")

# -------------------------------
# Padronização da chave
# -------------------------------
df_despesas["REG_ANS"] = (
    df_despesas["REG_ANS"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.strip()
)

df_cadastro["REGISTRO_OPERADORA"] = (
    df_cadastro["REGISTRO_OPERADORA"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.strip()
)

# -------------------------------
# Selecionar colunas necessárias do cadastro
# -------------------------------
df_cadastro = df_cadastro[[
    "REGISTRO_OPERADORA",
    "Razao_Social",
    "Modalidade",
    "UF"
]]

# Remover duplicidades no cadastro
df_cadastro = df_cadastro.drop_duplicates(subset="REGISTRO_OPERADORA")

print("REG_ANS exemplo:", df_despesas["REG_ANS"].head(5).tolist())
print("REGISTRO_OPERADORA exemplo:", df_cadastro["REGISTRO_OPERADORA"].head(5).tolist())

matches = df_despesas["REG_ANS"].isin(df_cadastro["REGISTRO_OPERADORA"]).sum()
print(f"Registros com match no cadastro: {matches}")

# -------------------------------
# JOIN (LEFT)
# -------------------------------
df_final = df_despesas.merge(
    df_cadastro,
    left_on="REG_ANS",
    right_on="REGISTRO_OPERADORA",
    how="left"
)

print(df_final[["REG_ANS", "Razao_Social", "UF"]].head(10))
print("Razão Social preenchida:", df_final["Razao_Social"].notna().sum())

# -------------------------------
# Tratar registros sem match
# -------------------------------
df_final["UF"] = df_final["UF"].fillna("Desconhecido")
df_final["Modalidade"] = df_final["Modalidade"].fillna("Desconhecida")

# -------------------------------
# Salvar CSV final
# -------------------------------
df_final.to_csv(output_file, sep=";", index=False, encoding="latin1")

print(" Enriquecimento concluído com sucesso!")
print(f"Arquivo gerado: {output_file}")
