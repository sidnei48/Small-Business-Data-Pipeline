import pandas as pd

ARQUIVO = "data/raw/AlunosTurma.xlsx"

df = pd.read_excel(
    ARQUIVO,
    sheet_name=0,
    header=None
)

codigos = pd.to_numeric(
    df[2],
    errors="coerce"
)

alunos = df.loc[
    codigos.notna(),
    [2, 3, 9]
].copy()

alunos = alunos.rename(
    columns={
        2: "codigo",
        3: "nome",
        9: "situacao"
    }
)

nulos_por_coluna = alunos.isna().sum()
total_nulos = nulos_por_coluna.sum()

print("Valores nulos por coluna:")
print(nulos_por_coluna)
print(f"\nTotal de valores nulos: {total_nulos}")