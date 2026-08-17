SELECT
    t.id_turma,
    t.nivel_livro,
    t.tipo_turma,
    COUNT(a.id_aluno) AS quantidade_alunos
FROM turma t
LEFT JOIN aluno a
    ON a.id_turma = t.id_turma
GROUP BY
    t.id_turma,
    t.nivel_livro,
    t.tipo_turma
ORDER BY t.id_turma;