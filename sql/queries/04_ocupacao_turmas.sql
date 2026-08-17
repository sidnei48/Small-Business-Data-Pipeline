SELECT
    t.id_turma,
    t.nivel_livro,
    t.tipo_turma,
    t.capacidade_maxima,
    COUNT(a.id_aluno) AS quantidade_alunos,
    ROUND(
        COUNT(a.id_aluno) * 100.0 / t.capacidade_maxima,
        2
    ) AS ocupacao_percentual
FROM turma t
LEFT JOIN aluno a
    ON a.id_turma = t.id_turma
GROUP BY
    t.id_turma,
    t.nivel_livro,
    t.tipo_turma,
    t.capacidade_maxima
ORDER BY ocupacao_percentual DESC;