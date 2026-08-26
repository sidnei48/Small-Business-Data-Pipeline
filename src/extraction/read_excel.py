import pandas as pd


arquivo = "data/raw/AlunosTurma.xlsx"

# Lê a planilha principal sem usar cabeçalho
df = pd.read_excel(
    arquivo,
    sheet_name="Sheet",
    header=None
)

# Mostra quantas linhas foram carregadas
print(f"Planilha carregada com sucesso: {len(df)} linhas.")