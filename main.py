import pandas as pd

# Carrega o arquivo csv / função que lê um arquivo de texto separado por vírgulas e o transforma em DataFrame.
df = pd.read_csv('BaseVarejo.csv')  #>Lê todo o arquivo
# df = pd.read_csv('BaseVarejo.csv', usecols=['valor', 'data_transacao']) #>Lê apenas as colunas selecionadas
# Mostra só as primeiras n linhas, útil para espiar a tabela sem imprimir tudo. head(n)

#df = pd.read_csv('BaseVarejo.csv', nrows=0)

# Mostra todas as colunas
pd.set_option("display.max_columns", None)
print(df.iloc[:, -3:].head())

print(df.head(10))
#print(df.info()) # tipos e nulos por coluna


print(df.columns)
