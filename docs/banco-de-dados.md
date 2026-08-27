# Banco de Dados

O projeto utiliza PostgreSQL para armazenar os dados tratados pelo pipeline.

A estrutura foi organizada em quatro tabelas principais:

- professor
- turma
- aluno
- matricula

## Tabela professor

Armazena os professores cadastrados.

Principais campos:

- `id_professor`: chave primária
- `nome`: nome do professor

Cada professor pode estar relacionado a várias turmas.

## Tabela turma

Armazena as informações das turmas.

Principais campos:

- `id_turma`: chave primária
- `nivel_livro`: nível ou livro utilizado
- `idioma`: idioma da turma
- `tipo_turma`: tipo da turma
- `dia_semana`: dia das aulas
- `horario_inicio`: horário inicial
- `capacidade_maxima`: quantidade máxima de alunos
- `id_professor`: chave estrangeira relacionada ao professor

Cada turma pertence a um professor e pode possuir várias matrículas.

## Tabela aluno

Armazena os alunos identificados na fonte de dados.

Principais campos:

- `id_aluno`: chave primária
- `nome`: nome do aluno

Um aluno pode possuir uma ou mais matrículas.

## Tabela matricula

Representa a relação entre alunos e turmas.

Principais campos:

- `id_matricula`: chave primária
- `id_aluno`: chave estrangeira relacionada ao aluno
- `id_turma`: chave estrangeira relacionada à turma
- `situacao`: situação da matrícula

A tabela de matrícula permite relacionar cada aluno à turma correspondente e registrar se a matrícula está ativa ou cancelada.

## Relacionamentos

Os relacionamentos principais são:

Professor 1:N Turma

Aluno 1:N Matricula

Turma 1:N Matricula

A tabela `matricula` funciona como ligação entre alunos e turmas.