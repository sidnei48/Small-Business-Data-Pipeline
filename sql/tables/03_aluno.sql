CREATE TABLE aluno (
    id_aluno INTEGER PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    situacao VARCHAR(30) NOT NULL,
    id_turma INTEGER NOT NULL,

    CONSTRAINT fk_aluno_turma
        FOREIGN KEY (id_turma)
        REFERENCES turma(id_turma)
);