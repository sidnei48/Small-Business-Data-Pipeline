import pandas as pd


ARQUIVO = "data/raw/AlunosTurma.xlsx"


df = pd.read_excel(
    ARQUIVO,
    sheet_name=0,
    header=None
)

linhas_turma = df[4].eq("Nº de alunos")

df["turma_origem"] = df[0].where(
    linhas_turma
).ffill()

codigos = pd.to_numeric(
    df[2],
    errors="coerce"
)

alunos = df.loc[
    codigos.notna(),
    [2, 3, 9, "turma_origem"]
].copy()

alunos = alunos.rename(
    columns={
        2: "codigo",
        3: "nome",
        9: "situacao"
    }
)

alunos["codigo"] = pd.to_numeric(
    alunos["codigo"]
).astype("int64")

total_registros = len(alunos)

alunos["prioridade_situacao"] = alunos["situacao"].map(
    {
        "Ativa": 1,
        "Cancelada": 2
    }
)

alunos = alunos.sort_values(
    by=[
        "codigo",
        "turma_origem",
        "prioridade_situacao"
    ]
)

alunos = alunos.drop_duplicates(
    subset=[
        "codigo",
        "turma_origem"
    ],
    keep="first"
)

alunos = alunos.drop(
    columns=["prioridade_situacao"]
)

total_alunos = alunos["codigo"].nunique()

total_matriculas_validas = len(alunos)

matriculas_ativas = (
    alunos["situacao"]
    .eq("Ativa")
    .sum()
)

matriculas_canceladas = (
    alunos["situacao"]
    .eq("Cancelada")
    .sum()
)

duplicados_removidos = (
    total_registros
    - total_matriculas_validas
)

capacidade_proxima_linha = df[6].shift(-1)

turmas_capacidade = df.loc[
    linhas_turma,
    [0]
].copy()

turmas_capacidade["capacidade_maxima"] = (
    capacidade_proxima_linha[linhas_turma]
)

turmas_capacidade = turmas_capacidade.rename(
    columns={
        0: "turma_origem"
    }
)

turmas_capacidade["capacidade_maxima"] = pd.to_numeric(
    turmas_capacidade["capacidade_maxima"],
    errors="coerce"
).astype("Int64")

total_turmas = (
    turmas_capacidade["turma_origem"]
    .nunique()
)

alunos_ativos = alunos.loc[
    alunos["situacao"].eq("Ativa")
].copy()

matriculas_ativas_por_turma = (
    alunos_ativos["turma_origem"]
    .value_counts()
)

ativos_por_turma = (
    matriculas_ativas_por_turma
    .reset_index()
)

ativos_por_turma = ativos_por_turma.rename(
    columns={
        "count": "alunos_ativos"
    }
)

ocupacao_turmas = turmas_capacidade.merge(
    ativos_por_turma,
    on="turma_origem",
    how="left"
)

ocupacao_turmas["alunos_ativos"] = (
    ocupacao_turmas["alunos_ativos"]
    .fillna(0)
    .astype("int64")
)

ocupacao_turmas["ocupacao_percentual"] = (
    ocupacao_turmas["alunos_ativos"]
    / ocupacao_turmas["capacidade_maxima"]
    * 100
)

ocupacao_turmas["ocupacao_percentual"] = (
    ocupacao_turmas["ocupacao_percentual"]
    .round(2)
)

ocupacao_turmas["vagas_disponiveis"] = (
    ocupacao_turmas["capacidade_maxima"]
    - ocupacao_turmas["alunos_ativos"]
)

total_sem_ativos = (
    ocupacao_turmas["alunos_ativos"]
    .eq(0)
    .sum()
)

turmas_lotadas = ocupacao_turmas.loc[
    ocupacao_turmas["vagas_disponiveis"].eq(0)
].copy()

total_turmas_lotadas = len(
    turmas_lotadas
)

turmas_acima_capacidade = ocupacao_turmas.loc[
    ocupacao_turmas["ocupacao_percentual"] > 100
].copy()

total_acima_capacidade = len(
    turmas_acima_capacidade
)

turmas_baixa_ocupacao = ocupacao_turmas.loc[
    ocupacao_turmas["ocupacao_percentual"] < 50
].copy()

total_baixa_ocupacao = len(
    turmas_baixa_ocupacao
)

media_matriculas_por_turma = (
    total_matriculas_validas
    / total_turmas
)

media_alunos_ativos_por_turma = (
    matriculas_ativas
    / total_turmas
)

print("\n=== INDICADORES ===")

print(f"Registros encontrados: {total_registros}")
print(f"Duplicados removidos: {duplicados_removidos}")
print(f"Alunos distintos: {total_alunos}")
print(f"Matrículas válidas: {total_matriculas_validas}")
print(f"Matrículas ativas: {matriculas_ativas}")
print(f"Matrículas canceladas: {matriculas_canceladas}")
print(f"Total de turmas: {total_turmas}")

print(
    f"Média de matrículas por turma: "
    f"{media_matriculas_por_turma:.2f}"
)

print(
    f"Média de alunos ativos por turma: "
    f"{media_alunos_ativos_por_turma:.2f}"
)

print(f"Turmas sem alunos ativos: {total_sem_ativos}")
print(f"Turmas lotadas: {total_turmas_lotadas}")
print(f"Turmas abaixo de 50% de ocupação: {total_baixa_ocupacao}")
print(f"Turmas acima da capacidade: {total_acima_capacidade}")