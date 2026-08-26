import pandas as pd


ARQUIVO = "data/raw/AlunosTurma.xlsx"


# Lê a planilha original
df = pd.read_excel(
    ARQUIVO,
    sheet_name=0,
    header=None
)

# Associa cada aluno à turma correspondente
df["turma_origem"] = df[0].where(
    df[4].eq("Nº de alunos")
).ffill()

# Converte os códigos para número
codigos = pd.to_numeric(
    df[2],
    errors="coerce"
)

# Mantém apenas as linhas que representam alunos
alunos = df.loc[
    codigos.notna(),
    [3, 9, "turma_origem"]
].copy()

# Adiciona o código do aluno já convertido para inteiro
alunos["codigo"] = codigos[
    codigos.notna()
].astype(int)

# Renomeia as colunas para facilitar a leitura
alunos = alunos.rename(
    columns={
        3: "nome",
        9: "situacao"
    }
)

# Organiza as colunas principais
alunos = alunos[
    ["codigo", "nome", "situacao", "turma_origem"]
]

# Dá prioridade para matrícula ativa em casos duplicados
alunos["prioridade_situacao"] = alunos["situacao"].map({
    "Ativa": 1,
    "Cancelada": 2
}).fillna(99)

# Guarda a quantidade de registros antes da limpeza
total_antes = len(alunos)

# Ordena e remove matrículas duplicadas do mesmo aluno na mesma turma
alunos_sem_duplicados = (
    alunos
    .sort_values(
        by=["codigo", "turma_origem", "prioridade_situacao"]
    )
    .drop_duplicates(
        subset=["codigo", "turma_origem"],
        keep="first"
    )
    .drop(columns=["prioridade_situacao"])
    .reset_index(drop=True)
)

# Guarda a quantidade de registros após a limpeza
total_depois = len(alunos_sem_duplicados)

# Exibe o resultado da remoção de duplicados
print(f"Registros antes da limpeza: {total_antes}")
print(f"Registros após a limpeza: {total_depois}")
print(f"Duplicados removidos: {total_antes - total_depois}")