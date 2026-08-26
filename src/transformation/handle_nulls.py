import pandas as pd


ARQUIVO = "data/raw/AlunosTurma.xlsx"


# Lê a planilha original
df = pd.read_excel(
    ARQUIVO,
    sheet_name=0,
    header=None
)

# Converte os códigos para número e ignora valores inválidos
codigos = pd.to_numeric(
    df[2],
    errors="coerce"
)

# Mantém apenas as linhas que representam alunos
alunos = df.loc[
    codigos.notna(),
    [2, 3, 9]
].copy()

# Renomeia as colunas para facilitar a leitura
alunos = alunos.rename(
    columns={
        2: "codigo",
        3: "nome",
        9: "situacao"
    }
)

# Conta os valores nulos de cada coluna
nulos_por_coluna = alunos.isna().sum()

# Soma todos os valores nulos encontrados
total_nulos = nulos_por_coluna.sum()

# Exibe o resultado da verificação
print("Valores nulos por coluna:")
print(nulos_por_coluna)

print(f"\nTotal de valores nulos: {total_nulos}")