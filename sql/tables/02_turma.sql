CREATE TABLE turma (
    id_turma SERIAL PRIMARY KEY,
    nivel_livro VARCHAR(100) NOT NULL,
    tipo_turma VARCHAR(20) NOT NULL,
    dia_semana VARCHAR(30) NOT NULL,
    horario_inicio TIME NOT NULL,
    capacidade_maxima INTEGER NOT NULL,
    id_professor INTEGER NOT NULL,

    CONSTRAINT fk_turma_professor
        FOREIGN KEY (id_professor)
        REFERENCES professor(id_professor)
);