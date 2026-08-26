from config.database import get_connection


# Insere os professores e ignora nomes que já existem
def inserir_professores(professores):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO professor (nome)
        VALUES (%s)
        ON CONFLICT (nome) DO NOTHING
    """

    for nome in professores:
        cursor.execute(
            sql,
            (nome,)
        )

    conn.commit()

    cursor.close()
    conn.close()


# Busca os IDs dos professores já cadastrados
def buscar_ids_professores():
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT id_professor, nome
        FROM professor
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()

    # Cria um dicionário no formato: nome -> id_professor
    ids_professores = {
        nome: id_professor
        for id_professor, nome in resultados
    }

    cursor.close()
    conn.close()

    return ids_professores


# Insere as turmas e atualiza a capacidade se ela mudar
def inserir_turmas(turmas):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO turma (
            nivel_livro,
            idioma,
            tipo_turma,
            dia_semana,
            horario_inicio,
            capacidade_maxima,
            id_professor
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (
            nivel_livro,
            idioma,
            tipo_turma,
            dia_semana,
            horario_inicio,
            id_professor
        )
        DO UPDATE SET
            capacidade_maxima = EXCLUDED.capacidade_maxima
    """

    # Percorre cada linha do DataFrame e envia os dados para o banco
    for turma in turmas.itertuples(index=False):
        cursor.execute(
            sql,
            (
                turma.nivel_livro,
                turma.idioma,
                turma.tipo_turma,
                turma.dia_semana,
                turma.horario_inicio,
                turma.capacidade_maxima,
                turma.id_professor
            )
        )

    conn.commit()

    cursor.close()
    conn.close()


# Insere os alunos e atualiza o nome caso já existam
def inserir_alunos(alunos_unicos):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO aluno (
            id_aluno,
            nome
        )
        VALUES (%s, %s)
        ON CONFLICT (id_aluno)
        DO UPDATE SET
            nome = EXCLUDED.nome
    """

    for aluno in alunos_unicos.itertuples(index=False):
        cursor.execute(
            sql,
            (
                aluno.codigo,
                aluno.nome
            )
        )

    conn.commit()

    cursor.close()
    conn.close()


# Busca os IDs das turmas já cadastradas
def buscar_ids_turmas():
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT
            id_turma,
            nivel_livro,
            idioma,
            tipo_turma,
            dia_semana,
            horario_inicio,
            id_professor
        FROM turma
    """

    cursor.execute(sql)

    resultados = cursor.fetchall()

    # Cria uma chave com os dados que identificam cada turma
    ids_turmas = {
        (
            nivel_livro,
            idioma,
            tipo_turma,
            dia_semana,
            horario_inicio.strftime("%H:%M"),
            id_professor
        ): id_turma
        for (
            id_turma,
            nivel_livro,
            idioma,
            tipo_turma,
            dia_semana,
            horario_inicio,
            id_professor
        ) in resultados
    }

    cursor.close()
    conn.close()

    return ids_turmas


# Insere as matrículas e atualiza a situação quando necessário
def inserir_matriculas(matriculas):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO matricula (
            id_aluno,
            id_turma,
            situacao
        )
        VALUES (%s, %s, %s)
        ON CONFLICT (
            id_aluno,
            id_turma
        )
        DO UPDATE SET
            situacao = EXCLUDED.situacao
    """

    for matricula in matriculas.itertuples(index=False):
        cursor.execute(
            sql,
            (
                matricula.codigo,
                matricula.id_turma,
                matricula.situacao
            )
        )

    conn.commit()

    cursor.close()
    conn.close()