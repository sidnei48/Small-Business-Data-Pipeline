from config.database import get_connection


def main():
    try:
        conn = get_connection()
        print("Conexão com PostgreSQL realizada com sucesso!")
        conn.close()
    except Exception as error:
        print("Erro ao conectar ao PostgreSQL:")
        print(error)


if __name__ == "__main__":
    main()