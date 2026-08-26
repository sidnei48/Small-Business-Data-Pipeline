import pandas as pd


ARQUIVO = "data/raw/AlunosTurma.xlsx"


# Lê a planilha original
df = pd.read_excel(
    ARQUIVO,
    sheet_name=0,
    header=None
)

# Converte os códigos para número
codigos = pd.to_numeric(
    df[2],
    errors="coerce"
)

# Mantém apenas as linhas que representam alunos
alunos = df.loc[
    codigos.notna(),
    [2, 3]
].copy()

# Renomeia as colunas para facilitar a leitura
alunos = alunos.rename(
    columns={
        2: "codigo",
        3: "nome"
    }
)

# Remove espaços extras no início, fim e entre palavras
alunos["nome_padronizado"] = (
    alunos["nome"]
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# Conta quantos nomes foram alterados
quantidade_alterados = (
    alunos["nome"] != alunos["nome_padronizado"]
).sum()

# Substitui o nome original pelo nome padronizado
alunos["nome"] = alunos["nome_padronizado"]

# Remove a coluna temporária usada na limpeza
alunos = alunos.drop(
    columns=["nome_padronizado"]
)

# Reinicia os índices depois do tratamento
alunos = alunos.reset_index(
    drop=True
)

# Exibe o resultado da padronização
print(f"Nomes padronizados: {quantidade_alterados}")
print(f"Total de registros processados: {len(alunos)}")