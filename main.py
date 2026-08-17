# importa a biblioteca pandas, nunpy e matplotlib.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carrega o arquivo csv / transforma arquivo em um DataFrame. 
  # sep=';': Define o ponto e vírgula (;)
  # encoding='utf-8-sig': Lê o arquivo com acentos corretos da língua portuguesa e remove marcas invisíveis no início do arquivo.
  # parse_dates=['DATA']: Converte a coluna 'DATA' para o tipo datetime.
  # dayfirst=True: Define que o formato da data é dia/mês/ano.
df = pd.read_csv('BaseVarejo.csv', sep=';', encoding='utf-8-sig', parse_dates=['DATA'], dayfirst=True,) 

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n PRIMEIRA ANALISE DO DATAFRAME\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

print(f">>> Total de {df.shape[0]} colunas.")
print(f">>> Total de {df.shape[1]} linhas.\n")
print(df.head(10)) # Mostrar as primeiras 10 linhas
print(df.info()) # tipos e nulos por coluna

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n     LIMPANDO O DATAFRAME    \nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

# Remove colunas que estão completamente em branco
  # usa how='all' para apagar a coluna que estiver totalmnete vazia
  # axis=1 para apagar a coluna, caso fosse axis=0 apagaria a linha
df_limpo = df.dropna(how='all', axis=1)
df_limpo = df_limpo.dropna(how='all', axis=0)
df_limpo = df_limpo.dropna(subset=['PR_CAT'], how='any') # Remove linhas com valores nulos na coluna PR_CAT

# Criação de um dicionário para renomear as colunas do DataFrame
converção_colunas = {
    'DATA': 'DataCompra',
    'CO_ID': 'id_Compra',
    'CL_ID': 'id_Cliente',
    'CL_GENERO': 'GeneroCliente',
    'CL_EC': 'EstadoCivil_Cl',
    'CL_FHL': 'Qtd_Filhos_Cl',
    'CL_SEG': 'SegmentoCliente',
    'PR_ID': 'id_Produto',
    'PR_CAT': 'CategoriaProduto',
    'PR_NOME': 'NomeProduto',
}
df_limpo=df_limpo.rename(columns=converção_colunas) #função renomear colunas com base no dicionário criado acima.
df_limpo.columns

# Contabilizando os tratamentos feitos nos dados
colunasExcluidas = df.shape[1] - df_limpo.shape[1]
print(f">>> Total de {colunasExcluidas} colunas excluidas.")
linhasExcluidas = df.shape[0] - df_limpo.shape[0]
print(f">>> Total de {linhasExcluidas} linhas excluidas.\n")

# Visualizando como ficou
print(df_limpo.head(10)) # Mostrar as primeiras 10 linhas do arquivo Limpo

# Salvar em um novo arquivo CSV (sem a coluna de índice)
df_limpo.to_csv('BaseVarejoLimpo.csv', index=False)

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nESTATÍSTICAS DESCRITIVAS columns:Qtd_Filhos_Cl\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

# 1. Carrega os dados
df_CadastroCliente = pd.read_csv('BaseVarejoLimpo.csv', usecols=['id_Cliente','GeneroCliente','EstadoCivil_Cl','Qtd_Filhos_Cl','SegmentoCliente'], index_col='id_Cliente')

# 2. Remove as duplicatas e atualiza o DataFrame
df_CadastroCliente = df_CadastroCliente.drop_duplicates()

# 3. Organiza o índice em ordem numérica crescente
df_CadastroCliente = df_CadastroCliente.sort_index(ascending=True)

# Salvar em um novo arquivo CSV (sem a coluna de índice)
df_CadastroCliente.to_csv('BaseCadastroClientes.csv', index=False)

filhos = df_CadastroCliente["Qtd_Filhos_Cl"].dropna()
print(f"• Mediana      : {filhos.median():.2f}")
print(f"• Desvio Padrão: {filhos.std():.2f}")
print(f"• Quartil 25%  : {filhos.quantile(0.25):.2f}")
print(f"• Quartil 50%  : {filhos.quantile(0.50):.2f}")
print(f"• Quartil 75%  : {filhos.quantile(0.75):.2f}")

print(f"• Média de filhos por Cliente : {filhos.mean():.2f}")
print(f"• Máximo de filhos por Cliente: {filhos.max()}")
print(f"• Mínimo de filhos por Cliente: {filhos.min()}")
print(f"• (Moda) A maioria dos Clientes tem:{filhos.mode()[0] if not filhos.mode().empty else 'N/A'} filhos")
print(f"• Total de Filhos de todos os Clientes : {filhos.sum().round(2)}")


print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n PADRÕES DE AGRUPAMENTOS \nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

def cor(data,target,columns):
    return ['#189BCC' if x in columns else "#EA213A" for x in sorted(data[target].unique())]


# Número total de compras por gênero do cliente
cat_por_cl = df_limpo.groupby(['GeneroCliente', 'CategoriaProduto'])['id_Compra'].nunique().reset_index()
color = cor(cat_por_cl, "GeneroCliente", ["M"])
quantidade_genero = pd.DataFrame(df_limpo["GeneroCliente"].value_counts())
g = sns.barplot(quantidade_genero.T, palette=color)
g.set_xlabel("Gênero")
g.set_ylabel("Compras")

# Demostração do grafico no VScode
print("\nNúmero total de compras por gênero do cliente:")
tabela_produto_por_genero = pd.pivot_table(
  df_limpo,
  index="CategoriaProduto",
  columns="GeneroCliente",
  values="id_Compra" if "id_Compra" in df_limpo.columns else "CategoriaProduto",
  aggfunc="count",
  fill_value=0
)
print(tabela_produto_por_genero)


# Mostra o grafico.
plt.show()

# Número de compras por número de filhos do cliente
media_filhos = pd.DataFrame(df_limpo.groupby(["Qtd_Filhos_Cl"])["id_Produto"].count()).reset_index()
g = sns.barplot(data=media_filhos,x="Qtd_Filhos_Cl",y="id_Produto")
g.set_ylabel("Contagem de compras")
g.set_xlabel("Número de Filhos")

# Demostração do grafico no VScode
print("\nNúmero de compras por número de filhos do cliente:")
tabela_categoria_por_filho = df_limpo.groupby("CategoriaProduto").agg(
  Total_Compras=("CategoriaProduto", "count"),
  Media_Filhos=("Qtd_Filhos_Cl", "mean") if "Qtd_Filhos_Cl" in df_limpo.columns else ("CategoriaProduto", "count")
).reset_index("CategoriaProduto").sort_values(by="Total_Compras", ascending=False)
    
print(tabela_categoria_por_filho)


# Mostra o grafico.
plt.show()

