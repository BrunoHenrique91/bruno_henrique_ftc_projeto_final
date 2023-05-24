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

st.set_page_config(page_title = '🌎 Visão País', layout = 'wide') 

# ======================== FIM =============================

# ======================= FUNÇÕES ==========================

def cal_top10 (df1, coluna_filtro):
            cols = ['nome_pais','Restaurant ID']
            filtro = df1.loc[(df1[coluna_filtro] == 0),:].copy()
            aux = filtro.loc[:,cols].groupby(['nome_pais', 'Restaurant ID']).count().reset_index()
            aux = (aux.groupby(['nome_pais']).
                                                                 count().sort_values(['Restaurant ID'], ascending = False).
                                                                 reset_index().head(10))
            return st.dataframe(aux)

def calc_media_pais(df1, coluna, nome_y):
    cols = ['nome_pais',coluna]
    aux1 = np.round(df1.loc[:,cols].groupby(['nome_pais']).mean().reset_index().sort_values([coluna], ascending = False),2)
    fig = px.bar(aux1, x='nome_pais', y=coluna, 
             labels = { 'nome_pais' : 'Paises', coluna : nome_y}, 
            hover_data=[coluna],color=coluna,
            text=coluna)
    return fig

def calculo_por_pais (df1, coluna, nome_y, filtro, coluna_filtro):
    if filtro == 0:
        cols = [coluna,'nome_pais']
        aux1 = df1.loc[:,cols].groupby(['nome_pais', coluna]).count().reset_index()
        aux2 = aux1.groupby(['nome_pais']).count().sort_values([coluna], ascending = False).reset_index() 
    else:
        filtro = df1.loc[(df1[coluna_filtro] == 4),:].copy()
        cols = [coluna,'nome_pais']
        aux1 = filtro.loc[:,cols].groupby(['nome_pais', coluna]).count().reset_index()
        aux2 = aux1.groupby(['nome_pais']).count().sort_values([coluna], ascending = False).reset_index() 
            
    fig = px.bar(aux2, x='nome_pais', y=coluna,
            labels = { 'nome_pais' : 'Paises', coluna : nome_y}, 
            hover_data=[coluna],color=coluna,
            text=coluna)
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

# VISÃO PAÍS

# ============= IMPORTANDO DF E LIMPANDO DF ================

df = pd.read_csv('zomato.csv')

df1 = limpando_df( df )

# ======================== FIM =============================

# =================== BARRA LATERAL ========================

st.header('🌎 Visão País')

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

st.sidebar.markdown('### Powered by Bruno Henrique')

# Linkando o  Filtro de país 
linhas_selecionadas = df1['nome_pais'].isin(countries_opions)
df1 = df1.loc[linhas_selecionadas,:]

# ======================== FIM =============================


# ====================== LAYOUT GRÁFICOS ==================
tab1, tab2, tab3 = st.tabs(['Visão Macro','Visão Macro 2', 'Países Top 10'])

with tab1:
    with st.container():
            fig = calculo_por_pais(df1, coluna = 'Restaurant ID',nome_y = 'Quantidade de Restaurantes', filtro = 0, coluna_filtro = '')
            fig.update_layout(title_text='Quantidade de Restaurantes Registrados por País', title_x=0.3)
            st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
            st.markdown("""___""")
            
    with st.container():
            fig = calculo_por_pais(df1, coluna = 'City',nome_y = 'Quantidade de Cidades', filtro = 0, coluna_filtro = '')
            fig.update_layout(title_text='Quantidade de Cidades por País', title_x=0.3)
            st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
            st.markdown("""___""")
                
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig = calc_media_pais(df1, coluna = 'Votes', nome_y='Média de Avaliações Feitas')
            fig.update_layout(title_text='Média de Avaliações feitas por País', title_x=0.3)
            st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
           
        with col2:
            fig = calc_media_pais(df1, coluna = 'Average Cost for two', nome_y='Preço média para duas pessoas')
            fig.update_layout(title_text='Média de Preço de um prato para duas pessoas por País', title_x=0.1)
            st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
        st.markdown("""___""")
        
with tab2:
    with st.container():
        fig = calc_media_pais(df1, coluna = 'Aggregate rating', nome_y='Média das Avaliaçõs')
        fig.update_layout(title_text='Média de Avaliação por País', title_x=0.3)
        st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
    st.markdown("""___""")
    
    with st.container():
        fig = calculo_por_pais(df1, coluna = 'Cuisines',nome_y = 'Quantidade Culinária Distinta', filtro =0, coluna_filtro = '' )
        fig.update_layout(title_text='Quantidade Culinária Distinta por País', title_x=0.3)
        st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
    st.markdown("""___""")
       
    with st.container():
        fig = calculo_por_pais(df1, coluna = 'Restaurant ID',nome_y = 'Quantidade Restaurante tipo Preço 4', filtro =1, coluna_filtro = 'Price range' )
        fig.update_layout(title_text='Quantidade Restaurante tipo Preço 4 por País', title_x=0.3)
        st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
    st.markdown("""___""")        
    
with tab3:
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('### Em Restaurantes que fazem entrega')
            cal_top10 (df1, coluna_filtro = 'Is delivering now' )
            
        with col2:
            st.markdown('### Em Restaurantes com entrega Online')
            cal_top10 (df1, coluna_filtro = 'Has Online delivery' )
            
        with col3:
            st.markdown('### Em Restaurantes que fazem Reserva')
            cal_top10 (df1, coluna_filtro = 'Has Table booking' )
