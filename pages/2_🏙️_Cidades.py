# ===================== IMPORTANDO LIBS ====================
import plotly.express as px
import folium
from haversine import haversine
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from streamlit_folium import folium_static
import streamlit as st
from PIL import Image


# ======================== FIM =============================

# ============== CONFIGURAÇÃO DA PÁGINA ====================

st.set_page_config(page_title = '🏙️ Visão Cidade', layout = 'wide') 

# ======================== FIM =============================

# ======================= FUNÇÕES ==========================

def cidades_tops(df1, coluna_filtro):
    cols = ['City','Restaurant ID']
    filtro = df1.loc[(df1[coluna_filtro] == 0),:].copy()
    aux = filtro.loc[:,cols].groupby('City').count().reset_index().sort_values('Restaurant ID', ascending = False).head(top_slider)
    return st.dataframe(aux)

def calc_top7_avg_cidades(df1, coluna, coluna_y, coluna_filtro, valor_filtro):
    cols = ['City',coluna, 'nome_pais']
    filtro = df1.loc[(df1[coluna_filtro] < valor_filtro),:].copy()
    aux = (filtro.loc[:,cols].groupby(['City', 'nome_pais']).count().reset_index().sort_values([coluna], ascending = False).head(top_slider))
    fig = px.bar(aux, x='City', y = coluna,labels = { 'City' : 'Cidades', coluna : coluna_y,'nome_pais' : 'Paises'}, 
                   color = 'nome_pais')
    return fig

def cal_top10_cidade (df1, coluna,nome_y):
    cols = ['City','nome_pais',coluna]
    aux = df1.loc[:,cols].groupby(['City','nome_pais']).count().reset_index().sort_values([coluna], ascending = False).head(top_slider)
    fig = px.bar(aux, x='City', y = coluna, labels = { 'City' : 'Cidades', coluna : nome_y,'nome_pais' : 'Paises'}, 
            color = 'nome_pais')
    return fig

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

# VISÃO CIDADES

# ============= IMPORTANDO DF E LIMPANDO DF ================

df = pd.read_csv('zomato.csv')

df1 = limpando_df( df )

# ======================== FIM =============================

# =================== BARRA LATERAL ========================

st.header('🏙️ Visão Cidade')

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

top_slider = st.sidebar.slider(
    'Selecione a quantidade de Restaurantes que deseja visualizar',
    value = 10,
    min_value = 1,
    max_value = 20)

st.sidebar.markdown("""___""")

st.sidebar.markdown('### Powered by Bruno Henrique')

# Linkando o  Filtro de país 
linhas_selecionadas = df1['nome_pais'].isin(countries_opions)
df1 = df1.loc[linhas_selecionadas,:]

# ======================== FIM =============================

# ====================== LAYOUT GRÁFICOS ==================
tab1, tab2 = st.tabs(['Indicadores','Top Cidades'])
    
with tab1:
    with st.container():
        fig = cal_top10_cidade (df1, coluna = 'Restaurant ID',nome_y = 'Quantidade Restaurantes')
        fig.update_layout(title_text=f'Top {top_slider} Cidades com mais Restaurantes', title_x=0.3)
        fig.update_traces(texttemplate = '%{y}',textposition='inside')
        st.plotly_chart(fig, use_container_width = True)

    with st.container():
        col1, col2 = st.columns(2)        

        with col1:
            fig = (calc_top7_avg_cidades(df1, coluna = 'Restaurant ID', coluna_y = 'Quantidade Restaurantes',coluna_filtro = 'Aggregate rating', valor_filtro = 4))
            fig.update_layout(title_text=f'Top {top_slider} Cidades com restaurantes com nota média acima de 4')
            fig.update_traces(texttemplate = '%{y}',textposition='inside')
            st.plotly_chart(fig, use_container_width = True)

        with col2:
            fig = (calc_top7_avg_cidades(df1, coluna = 'Restaurant ID', coluna_y = 'Quantidade Restaurantes',coluna_filtro = 'Aggregate rating', valor_filtro = 2.5))
            fig.update_layout(title_text=f'Top {top_slider} Cidades com restaurantes com nota média abaixo de 2,5', title_x=0.1)
            fig.update_traces(texttemplate = '%{y}',textposition='inside')
            st.plotly_chart(fig, use_container_width = True)

    with st.container():
        cols = [ 'City', 'Cuisines','nome_pais']
        cidade_culinaria = df1.loc[:,cols].groupby(['City', 'Cuisines','nome_pais']).count().reset_index()
        aux = cidade_culinaria.groupby(['City','nome_pais']).count().sort_values(['Cuisines'], ascending = False).reset_index().head(10)
        fig = px.bar(aux, x='City', y = 'Cuisines', title = 'Top 10 Cidades com Restauranyes com tipos de Culinária Distinta', 
                labels = { 'City' : 'Cidades', 'Cuisines' : 'Culinária','nome_pais' : 'Paises'}, 
               color = 'nome_pais')
        fig.update_layout(title_text=f'Top {top_slider} Cidades com Restaurantes com tipos de Culinária Distinta', title_x=0.1)
        fig.update_traces(texttemplate = '%{y}',textposition='inside')
        st.plotly_chart(fig, use_container_width = True)
        
with tab2:
    
     with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'### {top_slider} Em Restaurantes que aceitam reserva')
            cidades_tops (df1, coluna_filtro = 'Has Table booking' )
            
        with col2:
            st.markdown(f'### {top_slider} Em Restaurantes que fazem entrega')
            cidades_tops (df1, coluna_filtro = 'Is delivering now' )
        
        with col3:
            st.markdown(f'### {top_slider} Restaurantes que aceitam pedidos online')
            cidades_tops (df1, coluna_filtro = 'Has Online delivery' )
            
