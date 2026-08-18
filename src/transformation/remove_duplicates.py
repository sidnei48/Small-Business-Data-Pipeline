import pandas as pd


ARQUIVO = "data/raw/AlunosTurma.xlsx"


df = pd.read_excel(
    ARQUIVO,
    sheet_name="Sheet",
    header=None
)

df["turma_origem"] = df[0].where(
    df[4].eq("Nº de alunos")
).ffill()

codigos = pd.to_numeric(
    df[2],
    errors="coerce"
)

alunos = df.loc[
    codigos.notna(),
    [3, 9, "turma_origem"]
].copy()

alunos["codigo"] = codigos[
    codigos.notna()
].astype(int)

alunos = alunos.rename(
    columns={
        3: "nome",
        9: "situacao"
    }
)

alunos = alunos[
    ["codigo", "nome", "situacao", "turma_origem"]
]

alunos["prioridade_situacao"] = alunos["situacao"].map({
    "Ativa": 1,
    "Cancelada": 2
}).fillna(99)

total_antes = len(alunos)

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

total_depois = len(alunos_sem_duplicados)

print(f"Registros antes da limpeza: {total_antes}")
print(f"Registros após a limpeza: {total_depois}")
print(f"Duplicados removidos: {total_antes - total_depois}")