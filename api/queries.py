from src.config.database import get_connection


def buscar_indicadores():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM matricula
        WHERE situacao = 'Ativa'
    """)
    matriculas_ativas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM matricula
        WHERE situacao = 'Cancelada'
    """)
    matriculas_canceladas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT id_aluno)
        FROM matricula
        WHERE situacao = 'Ativa'
    """)
    alunos_ativos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM turma
    """)
    total_turmas = cursor.fetchone()[0]

    media_alunos_turma = (
        matriculas_ativas / total_turmas
        if total_turmas > 0
        else 0
    )

    cursor.close()
    conn.close()

    return {
        "matriculas_ativas": matriculas_ativas,
        "matriculas_canceladas": matriculas_canceladas,
        "alunos_ativos": alunos_ativos,
        "media_alunos_turma": round(media_alunos_turma, 2)
    }