import os

import psycopg

from dotenv import load_dotenv


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


# Cria e retorna uma conexão com o PostgreSQL
def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )