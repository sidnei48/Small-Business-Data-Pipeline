from fastapi import FastAPI

from api.queries import buscar_indicadores


app = FastAPI()


@app.get("/")
def home():
    return {
        "mensagem": "API funcionando"
    }


@app.get("/indicadores")
def indicadores():
    return buscar_indicadores()