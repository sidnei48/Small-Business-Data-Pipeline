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
        alunos = criar_colunas()

        if alunos.empty:
            raise ValueError(
                "Nenhum registro foi encontrado na fonte de dados."
            )

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

        if alunos[colunas_obrigatorias].isna().any().any():
            raise ValueError(
                "Existem valores nulos em campos obrigatórios."
            )

        situacoes_validas = [
            "Ativa",
            "Cancelada"
        ]

        situacoes_invalidas = ~alunos["situacao"].isin(
            situacoes_validas
        )

        if situacoes_invalidas.any():
            raise ValueError(
                "Existem situações de matrícula inválidas."
            )

        if (alunos["capacidade_maxima"] <= 0).any():
            raise ValueError(
                "Existem turmas com capacidade máxima inválida."
            )

        logger.info(
            f"Registros transformados: {len(alunos)}"
        )

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

        ids_professores = buscar_ids_professores()

        alunos["id_professor"] = (
            alunos["professor"]
            .map(ids_professores)
        )

        if alunos["id_professor"].isna().any():
            raise ValueError(
                "Existem professores sem id_professor."
            )

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

        colunas_identidade_turma = [
            "nivel_livro",
            "idioma",
            "tipo_turma",
            "dia_semana",
            "horario_inicio",
            "id_professor"
        ]

        if turmas.duplicated(
            subset=colunas_identidade_turma
        ).any():
            raise ValueError(
                "Existem turmas duplicadas ou com dados inconsistentes."
            )

        if turmas["turma_origem"].duplicated().any():
            raise ValueError(
                "Uma mesma turma possui informações inconsistentes."
            )

        inserir_turmas(turmas)

        logger.info(
            f"Turmas processadas: {len(turmas)}"
        )

        ids_turmas = buscar_ids_turmas()

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

        alunos["id_turma"] = (
            alunos["chave_turma"]
            .map(ids_turmas)
        )

        if alunos["id_turma"].isna().any():
            raise ValueError(
                "Existem registros sem id_turma."
            )

        alunos_unicos = alunos[
            [
                "codigo",
                "nome"
            ]
        ].drop_duplicates(
            subset=["codigo"]
        ).copy()

        if alunos_unicos["codigo"].duplicated().any():
            raise ValueError(
                "Existem códigos de alunos duplicados."
            )

        inserir_alunos(alunos_unicos)

        logger.info(
            f"Alunos processados: {len(alunos_unicos)}"
        )

        matriculas = alunos[
            [
                "codigo",
                "id_turma",
                "situacao"
            ]
        ].copy()

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

        matriculas = matriculas.drop_duplicates(
            subset=[
                "codigo",
                "id_turma"
            ],
            keep="first"
        )

        matriculas = matriculas.drop(
            columns=["prioridade_situacao"]
        )

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

    except Exception:
        logger.exception(
            "Erro durante a execução do pipeline"
        )
        raise


if __name__ == "__main__":
    main()