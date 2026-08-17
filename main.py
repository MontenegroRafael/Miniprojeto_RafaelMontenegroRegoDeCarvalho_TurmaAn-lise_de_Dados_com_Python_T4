# importa a biblioteca pandas.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

# Carrega o arquivo csv / transforma arquivo em um DataFrame. 
  # sep=';': Define o ponto e vírgula (;)
  # encoding='utf-8-sig': Lê o arquivo com acentos corretos da língua portuguesa e remove marcas invisíveis no início do arquivo.
  # parse_dates=['DATA']: Converte a coluna 'DATA' para o tipo datetime.
  # dayfirst=True: Define que o formato da data é dia/mês/ano.
df = pd.read_csv('BaseVarejo.csv', sep=';', encoding='utf-8-sig', parse_dates=['DATA'], dayfirst=True,) 

print(df.head(10)) # Mostrar as primeiras 10 linhas
print(df.info()) # tipos e nulos por coluna


#criação de um dicionário para renomear as colunas do DataFrame
converção_colunas = {
    'DATA': 'dt_Compra',
    'CO_ID': 'id_Compra',
    'CL_ID': 'id_Cliente',
    'CL_GENERO': 'genero_Cliente',
    'CL_EC': 'estadoCivil_Cliente',
    'CL_FHL': 'filhos_Cliente',
    'CL_SEG': 'segmento_Cliente',
    'PR_ID': 'id_Produto',
    'PR_CAT': 'categoria_Produto',
    'PR_NOME': 'nome_Produto',
}
df=df.rename(columns=converção_colunas) #função renomear colunas com base no dicionário criado acima.
df.columns

# Remove colunas que estão completamente em branco
  # usa how='all' para apagar a coluna que estiver totalmnete vazia
  # axis=1 para apagar a coluna, caso fosse axis=0 apagaria a linha
df_limpo = df.dropna(how='all', axis=1)

print("Valores nulos por coluna:")
print(df_limpo.isnull().sum()) # Mostrar a quantidade de valores nulos por coluna


# Salvar em um novo arquivo CSV (sem a coluna de índice)
df_limpo.to_csv('BaseVarejoLimpo.csv', index=False)
print(df_limpo.head(10)) # Mostrar as primeiras 10 linhas do novo arquivo limpo

# Contar quantas linhas duplicadas existem no total
total_duplicadas = df_limpo.duplicated().sum()

if total_duplicadas > 0:
  print(f"Foram encontradas {total_duplicadas} linhas duplicadas.")
  # Exibir as linhas duplicadas
  print(df_limpo[df_limpo.duplicated(keep=False)])
else:
  print("Não há linhas duplicadas neste arquivo.")

print(df_limpo.info()) # tipos e nulos por coluna no arquivo Limpo

# Verificar duplicadas com base em uma coluna específica
duplicadas_coluna = df_limpo.duplicated(subset=["nome_Produto","id_Compra"]).sum()
print(f"Duplicatas na coluna: {duplicadas_coluna}")
print(df_limpo[df_limpo.duplicated(keep=False)])



if "nome_Produto" in df_limpo.columns:
    print("\n1. Volume de Compras por Categoria:")
    agrupado_categoria = df_limpo.groupby("nome_Produto").agg(
        Total_Compras=("nome_Produto", "count"),
        Media_Filhos=("filhos_Cliente", "mean") 
        if "filhos_Cliente" in df_limpo.columns 
        else ("nome_Produto", "count")
    ).reset_index().sort_values(by="Total_Compras", ascending=False)
    
    print(agrupado_categoria)


# 2. Escolher as duas colunas
x = df_limpo['dt_Compra']
y = df_limpo['id_Compra']

# 3. Criar o gráfico (ex: linha ou barras)
plt.bar(x, y)  # Use plt.bar(x, y) se preferir gráfico de barras

# 4. Adicionar títulos
plt.title('Meu Gráfico')
plt.xlabel('Data da Compra')
plt.ylabel('ID da Compra')

# 5. Mostrar o gráfico na tela
plt.show()



'''

#, usecols=['DATA', 'CO_ID', 'CL_ID', 'CL_GENERO', 'CL_EC', 'CL_FHL', 'CL_SEG', 'PR_ID', 'PR_CAT', 'PR_NOME']
#, index_col='DATA'
df.describe() # Mostra estatísticas descritivas do DataFrame
print(df.describe()) # Mostra estatísticas descritivas do DataFrame
print("\nInformações das colunas:")
print(df.info())
print("\nValores nulos por coluna:")
print(df.isnull().sum())

df = pd.read_csv('BaseVarejo.csv', nrows=0)


pd.set_option("display.max_columns", None)
print(df.iloc[:, -3:].head())


print(df.info()) # tipos e nulos por coluna


print(df.columns)
'''