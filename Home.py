# ===================== IMPORTANDO LIBS ====================
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import folium
from haversine import haversine
import plotly.graph_objects as go
from streamlit_folium import folium_static
from PIL import Image
from folium.plugins import MarkerCluster


# ======================== FIM =============================

# ============== CONFIGURAÇÃO DA PÁGINA ====================

st.set_page_config(page_title = '📊 Home', layout = 'wide') 

# ======================== FIM =============================

def Building_Map(df1):

    df_new_ax = df1.groupby(by =['Restaurant Name', 'Cuisines','Latitude',
    'Longitude','Aggregate rating','nome_cor','Average Cost for two','Currency']).count().reset_index()[['Restaurant Name','Cuisines','Latitude', 'Longitude','Aggregate rating','nome_cor','Average Cost for two','Currency']]
    mapa = folium.Map()
    marcadores = MarkerCluster().add_to(mapa)
    for index, valor in df_new_ax.iterrows():

        latitude = valor ['Latitude']
        longitude = valor ['Longitude']
        infor = [valor ['Restaurant Name'], valor ['Cuisines'],valor ['Aggregate rating']]
        cor = valor['nome_cor']
        html = (f'''Nome: {valor ['Restaurant Name']}<br>
         <br>
Culinária: {valor ['Cuisines']}<br>
Prato p/ 2: {valor ['Average Cost for two']} / {valor ['Currency']}<br>
Avaliação: {valor ['Aggregate rating']}/5.0''')
        iframe = folium.IFrame(html,
                       width=260,
                       height=130)
        popup = folium.Popup(iframe,
                     max_width=260)

        folium.Marker(
        location = [latitude, longitude],
        popup = popup,
        icon = folium.Icon(color = cor)
        ).add_to(marcadores)

    folium_static(mapa, width = 1024 , height = 600)

# FUNÇÃO PARA INSERIR AS CORES NO DF

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

# FUNÇÃO PARA INSERIR OS NOMES DOS PÁISES NO DF

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    aux = COUNTRIES[country_id]
    
    return aux

# FUNÇÃO PARA CRIAR CATEGORIA D PREÇO

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
    
def limpando_df(df1):
    """ Esta Função faz a limpeza dos dados do DF e retorna um novo DF limpo.
        
        Tipos de Limpeza:
        1. Remoção dos Valores NaN
        2. Incluindo coluna do nome dos Países
        3. Incluindo coluna do nome das cores
        4. deixando apenas o nome da Culinária principal em 'Cuisines'
                
        Input: DataFrame
        Output: DataFrame    
    """
    # Removendo valores NaN
    df1.dropna(subset=['Cuisines'],inplace=True)
    
    #Ajustando a coluna Cuisines
    df1['Cuisines'] = df1['Cuisines'].astype(str)
    df1["Cuisines"] = df1.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])
    
    # Trocando id dos Países por nomes
    df1['nome_pais'] = df1['Country Code'].map(COUNTRIES)
    
    # Trocando id dos Países por nomes
    df1['nome_cor'] = df1['Rating color'].map(COLORS)
    
    return df1
    
# ======================== FIM =============================

# _______________INICIO DA LÓGICA DO CÓDIGO_________________

# Home

# ============= IMPORTANDO DF E LIMPANDO DF ================

df = pd.read_csv('zomato.csv')

df1 = limpando_df( df )
df2 = limpando_df( df )

# ======================== FIM =============================


# =================== BARRA LATERAL ========================

st.title('Fome Zero!')
st.header('O Melhor lugar para encontrar seu mais novo restaurante favorito!')

# Importando Logo na barra lateral
image_patch = 'logo.png'
image = Image.open(image_patch) #Comando para importar imagem da LIB PIL
st.sidebar.image(image, width = 250)

# Criando os primeiros elementos da barra lateral
st.sidebar.title('     Fome Zero') # Comando sidebar cria o botão da barra lateral
st.sidebar.markdown('## Conectando Clientes e Restaurantes')
st.sidebar.markdown("""___""")

# Criando filtro de tipo de trafego na barra lateral

st.sidebar.title('Filtros')
countries_opions = st.sidebar.multiselect(
    'Escolha os Países que deseja visualizar as informações :',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default = ['Brazil','United States of America','England', 'Qatar',
              'Australia','Canada'])

st.sidebar.markdown("""___""")

# Linkando o  Filtro de país 
linhas_selecionadas = df2['nome_pais'].isin(countries_opions)
df2 = df2.loc[linhas_selecionadas,:]

# ======================== FIM =============================

# ====================== LAYOUT GRÁFICOS ==================

with st.container():
    st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        cols = ['Restaurant ID']
        aux = df1.loc[:,cols]
        qtd_restaurantes = len(aux['Restaurant ID'].unique())     
        col1.metric('Restaurantes Cadastrados',qtd_restaurantes)
        
    with col2:
        cols = ['nome_pais']
        aux = df1.loc[:,cols]
        qtd_paises = len(aux['nome_pais'].unique())
        col2.metric('Países Cadastrados',qtd_paises)
        
    with col3:
        cols = ['City']
        aux = df1.loc[:,cols]
        qtd_cidade = len(aux['City'].unique())
        col3.metric('Cidades Cadastrados',qtd_cidade)
        
    with col4:
        cols = ['Votes']
        aux = df1.loc[:,cols]
        total_avaliacao = aux['Votes'].sum()
        col4.metric('Avaliações feitas na Plataforma',total_avaliacao)
        
    with col5:
        cols = ['Cuisines']
        aux = df1.loc[:,cols]
        total_culinaria = len(aux['Cuisines'].unique())
        col5.metric('Tipos de Culonária oferecidas',total_culinaria)

        
with st.container():
    Building_Map(df2)
  
