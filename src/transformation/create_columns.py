import pandas as pd


ARQUIVO = "data/raw/AlunosTurma.xlsx"


MAPA_DIAS = {
    "Seg": "Segunda",
    "Qua": "Quarta",
    "Quin": "Quinta",
    "Seg/Qua": "Segunda/Quarta",
    "Ter/Quin": "Terça/Quinta"
}


def normalizar_horario(valor):
    if pd.isna(valor):
        return pd.NA

    valor = str(valor).strip()

    if ":" in valor:
        hora, minuto = valor.split(":", maxsplit=1)
    else:
        hora = valor
        minuto = "00"

    return f"{int(hora):02d}:{int(minuto):02d}"


df = pd.read_excel(
    ARQUIVO,
    sheet_name=0,
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
).astype(int)


alunos["nome"] = (
    alunos["nome"]
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)


alunos["situacao"] = (
    alunos["situacao"]
    .str.strip()
)


alunos["turma_origem"] = (
    alunos["turma_origem"]
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.replace(r"\s*-\s*", " - ", regex=True)
)


partes_turma = alunos["turma_origem"].str.rsplit(
    " - ",
    n=2,
    expand=True
)


alunos["nivel_livro"] = (
    partes_turma[0]
    .str.replace(
        r"(?i)^vip\s*-\s*",
        "",
        regex=True
    )
    .str.replace(
        r"(?i)^vip\s+",
        "",
        regex=True
    )
    .str.strip()
)


alunos["dia_horario"] = (
    partes_turma[1]
    .str.strip()
)


alunos["professor"] = (
    partes_turma[2]
    .str.strip()
)


alunos["ativo"] = (
    alunos["situacao"]
    .eq("Ativa")
)


alunos["idioma"] = "Inglês"

alunos.loc[
    alunos["nivel_livro"]
    .str.lower()
    .str.startswith("espanhol"),
    "idioma"
] = "Espanhol"


eh_vip = (
    alunos["turma_origem"]
    .str.lower()
    .str.startswith("vip")
)


eh_pocket = (
    alunos["turma_origem"]
    .str.lower()
    .str.contains(r"\bpocket\b", regex=True)
)


alunos["tipo_turma"] = "Regular"

alunos.loc[
    eh_vip,
    "tipo_turma"
] = "VIP"

alunos.loc[
    eh_pocket,
    "tipo_turma"
] = "Pocket"

alunos.loc[
    eh_vip & eh_pocket,
    "tipo_turma"
] = "VIP Pocket"


alunos["dia_semana"] = (
    alunos["dia_horario"]
    .str.replace(
        r"\s+\d{1,2}(?::\d{2})?h(?:\s+[Pp]ocket)?$",
        "",
        regex=True
    )
    .str.strip()
    .replace(MAPA_DIAS)
)


horarios = alunos["dia_horario"].str.extract(
    r"(\d{1,2}(?::\d{2})?)h",
    expand=False
)


alunos["horario_inicio"] = (
    horarios.apply(normalizar_horario)
)


alunos = alunos.drop(
    columns=["dia_horario"]
)


alunos = alunos[
    [
        "codigo",
        "nome",
        "situacao",
        "ativo",
        "turma_origem",
        "nivel_livro",
        "idioma",
        "tipo_turma",
        "dia_semana",
        "horario_inicio",
        "professor"
    ]
]


alunos = alunos.reset_index(
    drop=True
)


colunas_geradas = [
    "nivel_livro",
    "idioma",
    "tipo_turma",
    "dia_semana",
    "horario_inicio",
    "professor"
]


total_nulos = (
    alunos[colunas_geradas]
    .isna()
    .sum()
    .sum()
)


print("Novas colunas criadas com sucesso.")

print(f"\nRegistros processados: {len(alunos)}")

print(f"Campos derivados nulos: {total_nulos}")

print("\nQuantidade por idioma:")
print(alunos["idioma"].value_counts())

print("\nQuantidade por tipo de turma:")
print(alunos["tipo_turma"].value_counts())

print("\nDias encontrados:")
print(
    alunos["dia_semana"]
    .value_counts()
    .sort_index()
)