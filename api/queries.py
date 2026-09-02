from src.config.database import get_connection


# Monta os filtros usados nas consultas do dashboard
def montar_filtros(
    professor=None,
    idioma=None,
    tipo_turma=None
):
    filtros = []
    parametros = []

    if professor:
        filtros.append("p.nome = %s")
        parametros.append(professor)

    if idioma:
        filtros.append("t.idioma = %s")
        parametros.append(idioma)

    if tipo_turma:
        filtros.append("t.tipo_turma = %s")
        parametros.append(tipo_turma)

    clausula_where = ""

    if filtros:
        clausula_where = " WHERE " + " AND ".join(filtros)

    return clausula_where, parametros


# Busca os principais indicadores apresentados nos cards
def buscar_indicadores(
    professor=None,
    idioma=None,
    tipo_turma=None
):
    sql = """
        SELECT
            COUNT(m.id_matricula) FILTER (
                WHERE m.situacao = 'Ativa'
            ),
            COUNT(m.id_matricula) FILTER (
                WHERE m.situacao = 'Cancelada'
            ),
            COUNT(DISTINCT m.id_aluno) FILTER (
                WHERE m.situacao = 'Ativa'
            ),
            COUNT(DISTINCT t.id_turma)
        FROM turma t
        JOIN professor p
            ON p.id_professor = t.id_professor
        LEFT JOIN matricula m
            ON m.id_turma = t.id_turma
    """

    where, parametros = montar_filtros(
        professor,
        idioma,
        tipo_turma
    )

    sql += where

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                parametros
            )

            resultado = cursor.fetchone()

    matriculas_ativas = resultado[0]
    matriculas_canceladas = resultado[1]
    alunos_ativos = resultado[2]
    total_turmas = resultado[3]

    media_alunos_turma = (
        matriculas_ativas / total_turmas
        if total_turmas > 0
        else 0
    )

    return {
        "matriculas_ativas": matriculas_ativas,
        "matriculas_canceladas": matriculas_canceladas,
        "alunos_ativos": alunos_ativos,
        "media_alunos_turma": round(
            media_alunos_turma,
            2
        )
    }


# Busca as opções disponíveis nos filtros do dashboard
def buscar_filtros():
    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT nome
                FROM professor
                ORDER BY nome
            """)

            professores = [
                resultado[0]
                for resultado in cursor.fetchall()
            ]

            cursor.execute("""
                SELECT DISTINCT idioma
                FROM turma
                ORDER BY idioma
            """)

            idiomas = [
                resultado[0]
                for resultado in cursor.fetchall()
            ]

            cursor.execute("""
                SELECT DISTINCT tipo_turma
                FROM turma
                ORDER BY tipo_turma
            """)

            tipos_turma = [
                resultado[0]
                for resultado in cursor.fetchall()
            ]

    return {
        "professores": professores,
        "idiomas": idiomas,
        "tipos_turma": tipos_turma
    }


# Conta os alunos ativos relacionados a cada professor
def buscar_alunos_por_professor(
    professor=None,
    idioma=None,
    tipo_turma=None
):
    sql = """
        SELECT
            p.nome,
            COUNT(DISTINCT m.id_aluno) FILTER (
                WHERE m.situacao = 'Ativa'
            ) AS alunos_ativos
        FROM professor p
        JOIN turma t
            ON t.id_professor = p.id_professor
        LEFT JOIN matricula m
            ON m.id_turma = t.id_turma
    """

    where, parametros = montar_filtros(
        professor,
        idioma,
        tipo_turma
    )

    sql += where

    sql += """
        GROUP BY
            p.id_professor,
            p.nome
        ORDER BY
            alunos_ativos DESC
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                parametros
            )

            resultados = cursor.fetchall()

    return {
        "professores": [
            resultado[0]
            for resultado in resultados
        ],
        "alunos_ativos": [
            resultado[1]
            for resultado in resultados
        ]
    }


# Conta quantas turmas existem em cada tipo
def buscar_turmas_por_tipo(
    professor=None,
    idioma=None,
    tipo_turma=None
):
    sql = """
        SELECT
            t.tipo_turma,
            COUNT(DISTINCT t.id_turma) AS quantidade_turmas
        FROM turma t
        JOIN professor p
            ON p.id_professor = t.id_professor
    """

    where, parametros = montar_filtros(
        professor,
        idioma,
        tipo_turma
    )

    sql += where

    sql += """
        GROUP BY
            t.tipo_turma
        ORDER BY
            quantidade_turmas DESC
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                parametros
            )

            resultados = cursor.fetchall()

    return {
        "tipos_turma": [
            resultado[0]
            for resultado in resultados
        ],
        "quantidades": [
            resultado[1]
            for resultado in resultados
        ]
    }


# Calcula o percentual de ocupação de cada turma
def buscar_ocupacao_turmas(
    professor=None,
    idioma=None,
    tipo_turma=None
):
    sql = """
        SELECT
            t.id_turma,
            t.nivel_livro,
            t.dia_semana,
            t.capacidade_maxima,
            COUNT(m.id_matricula) FILTER (
                WHERE m.situacao = 'Ativa'
            ) AS alunos_ativos
        FROM turma t
        JOIN professor p
            ON p.id_professor = t.id_professor
        LEFT JOIN matricula m
            ON m.id_turma = t.id_turma
    """

    where, parametros = montar_filtros(
        professor,
        idioma,
        tipo_turma
    )

    sql += where

    sql += """
        GROUP BY
            t.id_turma,
            t.nivel_livro,
            t.dia_semana,
            t.capacidade_maxima
        ORDER BY
            (
                COUNT(m.id_matricula) FILTER (
                    WHERE m.situacao = 'Ativa'
                )
            )::decimal
            / NULLIF(t.capacidade_maxima, 0) DESC
            NULLS LAST
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                parametros
            )

            resultados = cursor.fetchall()

    turmas = []
    ocupacoes = []

    for resultado in resultados:
        id_turma = resultado[0]
        nivel_livro = resultado[1]
        dia_semana = resultado[2]
        capacidade = resultado[3]
        alunos_ativos = resultado[4]

        ocupacao = (
            alunos_ativos / capacidade * 100
            if capacidade > 0
            else 0
        )

        nome_turma = (
            f"{id_turma} - "
            f"{nivel_livro} - "
            f"{dia_semana}"
        )

        turmas.append(nome_turma)
        ocupacoes.append(
            round(ocupacao, 1)
        )

    return {
        "turmas": turmas,
        "ocupacoes": ocupacoes
    }