import pandas as pd

arquivo = "tests/data/alunos_teste.csv"

df = pd.read_csv(arquivo)

print(f"CSV carregado com sucesso: {len(df)} registros.")