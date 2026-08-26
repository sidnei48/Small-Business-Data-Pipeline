import pandas as pd


arquivo = "tests/data/alunos_teste.csv"

# Lê o arquivo CSV de teste
df = pd.read_csv(arquivo)

# Mostra quantos registros foram carregados
print(f"CSV carregado com sucesso: {len(df)} registros.")