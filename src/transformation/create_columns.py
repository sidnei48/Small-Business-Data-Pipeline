import pandas as pd


ARQUIVO = "data/raw/AlunosTurma.xlsx"


# Converte as abreviações dos dias para nomes completos
MAPA_DIAS = {
    "Seg": "Segunda",
    "Qua": "Quarta",
    "Quin": "Quinta",
    "Seg/Qua": "Segunda/Quarta",
    "Ter/Quin": "Terça/Quinta"
}


# Padroniza os horários para o formato HH:MM
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


def criar_colunas():
    # Lê a planilha original
    df = pd.read_excel(
        ARQUIVO,
        sheet_name=0,
        header=None
    )

    # Identifica as linhas que representam o início de uma turma
    linhas_turma = df[4].eq("Nº de alunos")

    # A capacidade da turma está na linha seguinte
    capacidade_proxima_linha = df[6].shift(-1)

    # Preenche cada aluno com a capacidade da sua turma
    df["capacidade_maxima"] = capacidade_proxima_linha.where(
        linhas_turma
    ).ffill()

    # Preenche cada aluno com o nome da turma correspondente
    df["turma_origem"] = df[0].where(
        linhas_turma
    ).ffill()

    # Converte os códigos para número e ignora linhas que não são alunos
    codigos = pd.to_numeric(
        df[2],
        errors="coerce"
    )

    # Mantém apenas os dados necessários dos alunos
    alunos = df.loc[
        codigos.notna(),
        [2, 3, 9, "turma_origem", "capacidade_maxima"]
    ].copy()

    # Renomeia as colunas para facilitar o uso
    alunos = alunos.rename(
        columns={
            2: "codigo",
            3: "nome",
            9: "situacao"
        }
    )

    # Ajusta os tipos dos campos numéricos
    alunos["codigo"] = pd.to_numeric(
        alunos["codigo"]
    ).astype(int)

    alunos["capacidade_maxima"] = pd.to_numeric(
        alunos["capacidade_maxima"]
    ).astype("int64")

    # Remove espaços extras dos nomes
    alunos["nome"] = (
        alunos["nome"]
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    # Remove espaços extras da situação da matrícula
    alunos["situacao"] = (
        alunos["situacao"]
        .str.strip()
    )

    # Padroniza o texto usado para identificar as turmas
    alunos["turma_origem"] = (
        alunos["turma_origem"]
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"\s*-\s*", " - ", regex=True)
    )

    # Separa nível, dia/horário e professor
    partes_turma = alunos["turma_origem"].str.rsplit(
        " - ",
        n=2,
        expand=True
    )

    # Remove o texto VIP para manter apenas o nível do livro
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

    # Cria uma coluna booleana indicando matrícula ativa
    alunos["ativo"] = (
        alunos["situacao"]
        .eq("Ativa")
    )

    # Define Inglês como idioma padrão
    alunos["idioma"] = "Inglês"

    # Identifica as turmas de Espanhol
    alunos.loc[
        alunos["nivel_livro"]
        .str.lower()
        .str.startswith("espanhol"),
        "idioma"
    ] = "Espanhol"

    # Identifica turmas VIP
    eh_vip = (
        alunos["turma_origem"]
        .str.lower()
        .str.startswith("vip")
    )

    # Identifica turmas Pocket
    eh_pocket = (
        alunos["turma_origem"]
        .str.lower()
        .str.contains(r"\bpocket\b", regex=True)
    )

    # Define o tipo padrão da turma
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

    # Separa o dia da semana do horário
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

    # Extrai apenas o horário da turma
    horarios = alunos["dia_horario"].str.extract(
        r"(\d{1,2}(?::\d{2})?)h",
        expand=False
    )

    # Padroniza os horários encontrados
    alunos["horario_inicio"] = (
        horarios.apply(normalizar_horario)
    )

    # Remove a coluna temporária usada na separação
    alunos = alunos.drop(
        columns=["dia_horario"]
    )

    # Organiza as colunas finais do DataFrame
    alunos = alunos[
        [
            "codigo",
            "nome",
            "situacao",
            "ativo",
            "turma_origem",
            "capacidade_maxima",
            "nivel_livro",
            "idioma",
            "tipo_turma",
            "dia_semana",
            "horario_inicio",
            "professor"
        ]
    ]

    # Reinicia os índices após a transformação
    alunos = alunos.reset_index(
        drop=True
    )

    return alunos