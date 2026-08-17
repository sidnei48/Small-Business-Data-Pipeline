SELECT
    a.id_aluno,
    a.nome,
    a.situacao,
    t.nivel_livro,
    t.tipo_turma,
    t.dia_semana,
    t.horario_inicio
FROM aluno a
INNER JOIN turma t
    ON a.id_turma = t.id_turma;