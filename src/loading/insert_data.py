from config.database import get_connection


def inserir_professores(professores):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO professor (nome)
        VALUES (%s)
    """

    for nome in professores:
        cursor.execute(
            sql,
            (nome,)
        )

    conn.commit()

    cursor.close()
    conn.close()