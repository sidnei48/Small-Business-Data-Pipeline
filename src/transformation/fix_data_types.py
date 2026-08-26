import pandas as pd


ARQUIVO = "data/raw/AlunosTurma.xlsx"


# Lê a planilha original
df = pd.read_excel(
    ARQUIVO,
    sheet_name=0,
    header=None
)

# Tenta converter os códigos para número
codigos = pd.to_numeric(
    df[2],
    errors="coerce"
)

# Mantém apenas as linhas que representam alunos
alunos = df.loc[
    codigos.notna(),
    [2, 3, 9]
].copy()

# Renomeia as colunas para facilitar o uso
alunos = alunos.rename(
    columns={
        2: "codigo",
        3: "nome",
        9: "situacao"
    }
)

# Corrige o tipo da coluna código para inteiro
alunos["codigo"] = pd.to_numeric(
    alunos["codigo"]
).astype(int)

# Confirma os tipos finais das colunas
print("Tipos de dados corrigidos com sucesso.")
print(alunos.dtypes)