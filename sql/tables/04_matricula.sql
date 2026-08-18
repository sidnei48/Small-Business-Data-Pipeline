CREATE TABLE matricula (
    id_matricula SERIAL PRIMARY KEY,
    id_aluno INTEGER NOT NULL,
    id_turma INTEGER NOT NULL,
    situacao VARCHAR(30) NOT NULL,

    CONSTRAINT fk_matricula_aluno
        FOREIGN KEY (id_aluno)
        REFERENCES aluno(id_aluno),

    CONSTRAINT fk_matricula_turma
        FOREIGN KEY (id_turma)
        REFERENCES turma(id_turma)
);