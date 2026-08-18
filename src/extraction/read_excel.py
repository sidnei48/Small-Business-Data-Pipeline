import pandas as pd

arquivo = "data/raw/AlunosTurma.xlsx"

df = pd.read_excel(
    arquivo,
    sheet_name="Sheet",
    header=None
)

print(f"Planilha carregada com sucesso: {len(df)} linhas.")
