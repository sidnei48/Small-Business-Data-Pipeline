from fastapi import FastAPI

from api.queries import (
    buscar_indicadores,
    buscar_filtros,
    buscar_alunos_por_professor,
    buscar_turmas_por_tipo,
    buscar_ocupacao_turmas
)


# Cria a API usada pelo dashboard
app = FastAPI(
    title="Small Business Data Pipeline API",
    version="1.0.0"
)


# Rota usada para verificar se a API está funcionando
@app.get("/")
def home():
    return {
        "mensagem": "API funcionando"
    }


# Retorna os principais indicadores do dashboard
@app.get("/indicadores")
def indicadores(
    professor: str | None = None,
    idioma: str | None = None,
    tipo_turma: str | None = None
):
    return buscar_indicadores(
        professor,
        idioma,
        tipo_turma
    )


# Retorna as opções disponíveis nos filtros
@app.get("/filtros")
def filtros():
    return buscar_filtros()


# Retorna a quantidade de alunos ativos por professor
@app.get("/graficos/alunos-professor")
def alunos_professor(
    professor: str | None = None,
    idioma: str | None = None,
    tipo_turma: str | None = None
):
    return buscar_alunos_por_professor(
        professor,
        idioma,
        tipo_turma
    )


# Retorna a quantidade de turmas por tipo
@app.get("/graficos/turmas-tipo")
def turmas_tipo(
    professor: str | None = None,
    idioma: str | None = None,
    tipo_turma: str | None = None
):
    return buscar_turmas_por_tipo(
        professor,
        idioma,
        tipo_turma
    )


# Retorna o percentual de ocupação das turmas
@app.get("/graficos/ocupacao-turmas")
def ocupacao_turmas(
    professor: str | None = None,
    idioma: str | None = None,
    tipo_turma: str | None = None
):
    return buscar_ocupacao_turmas(
        professor,
        idioma,
        tipo_turma
    )