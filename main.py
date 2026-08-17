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

produtos_mais_vendidos = pd.DataFrame(df_limpo.groupby(["CategoriaProduto","NomeProduto"])["id_Produto"].count().reset_index())
#produtos_mais_vendidos = produtos_mais_vendidos.drop(produtos_mais_vendidos["CategoriaProduto"]=="#N/D")
produtos_mais_vendidos = produtos_mais_vendidos[produtos_mais_vendidos["CategoriaProduto"] != "#N/D"]
produtos_mais_vendidos = produtos_mais_vendidos.rename(columns={"id_Produto":"Contagem","CategoriaProduto":"Categoria","PR_NOME":"Nome do produto"})
produtos_mais_vendidos = produtos_mais_vendidos.groupby("Categoria").apply(lambda x: x.nlargest(1,"Contagem"))

produtos_mais_vendidos = produtos_mais_vendidos.drop(columns=["Categoria"]).reset_index()
sns.barplot(data=produtos_mais_vendidos,x="Nome do produto",y="Contagem")
plt.xticks(rotation=45)
plt.title("Maior ocorrencia de vendas em cada categoria")
