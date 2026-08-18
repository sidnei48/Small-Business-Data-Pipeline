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
    [2, 3]
].copy()

alunos = alunos.rename(
    columns={
        2: "codigo",
        3: "nome"
    }
)

alunos["nome_padronizado"] = (
    alunos["nome"]
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

quantidade_alterados = (
    alunos["nome"] != alunos["nome_padronizado"]
).sum()

alunos["nome"] = alunos["nome_padronizado"]

alunos = alunos.drop(
    columns=["nome_padronizado"]
)

alunos = alunos.reset_index(
    drop=True
)

print(f"Nomes padronizados: {quantidade_alterados}")
print(f"Total de registros processados: {len(alunos)}")