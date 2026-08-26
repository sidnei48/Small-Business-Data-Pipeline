from transformation.create_columns import criar_colunas
from utils.logger import logger
from loading.insert_data import (
    inserir_professores,
    buscar_ids_professores,
    inserir_turmas,
    inserir_alunos,
    buscar_ids_turmas,
    inserir_matriculas
)


def main():
    logger.info("Pipeline iniciado")

    try:
        # Carrega e transforma os dados da planilha
        alunos = criar_colunas()

        # Garante que a fonte não esteja vazia
        if alunos.empty:
            raise ValueError(
                "Nenhum registro foi encontrado na fonte de dados."
            )

        # Campos que precisam estar preenchidos para o pipeline funcionar
        colunas_obrigatorias = [
            "codigo",
            "nome",
            "situacao",
            "turma_origem",
            "nivel_livro",
            "idioma",
            "tipo_turma",
            "dia_semana",
            "horario_inicio",
            "capacidade_maxima",
            "professor"
        ]

        # Impede que dados importantes vazios sigam para o banco
        if alunos[colunas_obrigatorias].isna().any().any():
            raise ValueError(
                "Existem valores nulos em campos obrigatórios."
            )

        # Situações aceitas para uma matrícula
        situacoes_validas = [
            "Ativa",
            "Cancelada"
        ]

        situacoes_invalidas = ~alunos["situacao"].isin(
            situacoes_validas
        )

        # Para o pipeline se encontrar uma situação inesperada
        if situacoes_invalidas.any():
            raise ValueError(
                "Existem situações de matrícula inválidas."
            )

        # Evita turmas com capacidade impossível
        if (alunos["capacidade_maxima"] <= 0).any():
            raise ValueError(
                "Existem turmas com capacidade máxima inválida."
            )

        logger.info(
            f"Registros transformados: {len(alunos)}"
        )

        # Cria uma lista com professores sem repetição
        professores = (
            alunos["professor"]
            .dropna()
            .drop_duplicates()
            .tolist()
        )

        inserir_professores(professores)

        logger.info(
            f"Professores processados: {len(professores)}"
        )

        # Busca os IDs gerados no banco para cada professor
        ids_professores = buscar_ids_professores()

        alunos["id_professor"] = (
            alunos["professor"]
            .map(ids_professores)
        )

        # Confere se todos os professores encontraram um ID
        if alunos["id_professor"].isna().any():
            raise ValueError(
                "Existem professores sem id_professor."
            )

        # Separa as turmas únicas que serão enviadas ao banco
        turmas = alunos[
            [
                "turma_origem",
                "nivel_livro",
                "idioma",
                "tipo_turma",
                "dia_semana",
                "horario_inicio",
                "capacidade_maxima",
                "id_professor"
            ]
        ].drop_duplicates().copy()

        # Campos usados para identificar uma turma
        colunas_identidade_turma = [
            "nivel_livro",
            "idioma",
            "tipo_turma",
            "dia_semana",
            "horario_inicio",
            "id_professor"
        ]

        # Evita duas turmas com a mesma identificação
        if turmas.duplicated(
            subset=colunas_identidade_turma
        ).any():
            raise ValueError(
                "Existem turmas duplicadas ou com dados inconsistentes."
            )

        # Confere se o mesmo nome de origem não possui informações diferentes
        if turmas["turma_origem"].duplicated().any():
            raise ValueError(
                "Uma mesma turma possui informações inconsistentes."
            )

        inserir_turmas(turmas)

        logger.info(
            f"Turmas processadas: {len(turmas)}"
        )

        # Busca os IDs das turmas que já estão no banco
        ids_turmas = buscar_ids_turmas()

        # Cria uma chave com os dados que identificam cada turma
        alunos["chave_turma"] = list(
            zip(
                alunos["nivel_livro"],
                alunos["idioma"],
                alunos["tipo_turma"],
                alunos["dia_semana"],
                alunos["horario_inicio"],
                alunos["id_professor"]
            )
        )

        # Liga cada matrícula ao ID correto da turma
        alunos["id_turma"] = (
            alunos["chave_turma"]
            .map(ids_turmas)
        )

        # Garante que nenhuma matrícula ficou sem turma
        if alunos["id_turma"].isna().any():
            raise ValueError(
                "Existem registros sem id_turma."
            )

        # Mantém apenas uma linha por aluno
        alunos_unicos = alunos[
            [
                "codigo",
                "nome"
            ]
        ].drop_duplicates(
            subset=["codigo"]
        ).copy()

        # Confere se ainda existe algum código repetido
        if alunos_unicos["codigo"].duplicated().any():
            raise ValueError(
                "Existem códigos de alunos duplicados."
            )

        inserir_alunos(alunos_unicos)

        logger.info(
            f"Alunos processados: {len(alunos_unicos)}"
        )

        # Prepara apenas os dados necessários para a matrícula
        matriculas = alunos[
            [
                "codigo",
                "id_turma",
                "situacao"
            ]
        ].copy()

        # Dá prioridade para matrícula ativa quando existir duplicidade
        matriculas["prioridade_situacao"] = (
            matriculas["situacao"].map(
                {
                    "Ativa": 1,
                    "Cancelada": 2
                }
            )
        )

        matriculas = matriculas.sort_values(
            by=[
                "codigo",
                "id_turma",
                "prioridade_situacao"
            ]
        )

        # Mantém apenas uma matrícula por aluno e turma
        matriculas = matriculas.drop_duplicates(
            subset=[
                "codigo",
                "id_turma"
            ],
            keep="first"
        )

        # Remove a coluna temporária usada na limpeza
        matriculas = matriculas.drop(
            columns=["prioridade_situacao"]
        )

        # Confere se ainda restou alguma matrícula duplicada
        if matriculas.duplicated(
            subset=[
                "codigo",
                "id_turma"
            ]
        ).any():
            raise ValueError(
                "Existem matrículas duplicadas."
            )

        campos_matricula = [
            "codigo",
            "id_turma",
            "situacao"
        ]

        # Última validação antes de enviar as matrículas ao banco
        if matriculas[campos_matricula].isna().any().any():
            raise ValueError(
                "Existem matrículas com campos obrigatórios ausentes."
            )

        inserir_matriculas(matriculas)

        logger.info(
            f"Matrículas processadas: {len(matriculas)}"
        )

        logger.info(
            "Pipeline finalizado com sucesso"
        )

    # Registra qualquer erro que interrompa o pipeline
    except Exception:
        logger.exception(
            "Erro durante a execução do pipeline"
        )
        raise


if __name__ == "__main__":
    main()