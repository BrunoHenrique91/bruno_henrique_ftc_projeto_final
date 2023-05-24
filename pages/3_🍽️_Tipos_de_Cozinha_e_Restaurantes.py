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

st.set_page_config(page_title = '🍽️ Visão Tipos de Cusinhas', layout = 'wide') 

# ======================== FIM =============================

# ======================= FUNÇÕES ==========================

def calc_cuisines(df1, coluna, name_y, filtro_entregas):
    if filtro_entregas == 1:
        cols = ['Cuisines',coluna]
        filtro = df1.loc[((df1['Has Online delivery'] == 0) & (df1['Is delivering now'] == 0)),:].copy()
        aux = filtro.loc[:,cols].groupby(['Cuisines']).count().reset_index().sort_values(coluna,ascending = False).head(top_slider)
        fig = px.bar(aux, x='Cuisines', y=coluna, labels = { 'Cuisines' : 'Tipos de Culinária', coluna : name_y},hover_data=[coluna],color=coluna,text=coluna)
    else:
        cols = ['Cuisines', coluna]
        aux = np.round(df1.loc[:,cols].groupby(['Cuisines']).mean().reset_index().sort_values(coluna,ascending = False),2).head(top_slider)
        fig = px.bar(aux, x='Cuisines', y=coluna, labels = { 'Cuisines' : 'Tipos de Culinária', coluna : name_y},hover_data=[coluna],color=coluna,text=coluna)  
    return fig

def calc_restaurantes(df1, coluna, filtro, nome_y ):
    if filtro == 0:
        cols = ['Restaurant Name',coluna,'Restaurant ID']
        aux = df1.loc[:,cols].groupby(['Restaurant Name','Restaurant ID']).mean().reset_index().sort_values([coluna,'Restaurant ID'],ascending = [False,True]).head(10)
        fig = px.bar(aux, x= 'Restaurant Name', y=coluna, labels = { 'Restaurant Name' : 'Restaurante', coluna : nome_y},hover_data=[coluna],color=coluna,text=coluna)
    else:
        cols = ['Restaurant Name',coluna,'Restaurant ID']
        aux = df1.loc[:,cols].groupby(['Restaurant Name','Restaurant ID']).sum().reset_index().sort_values([coluna,'Restaurant ID'],ascending = [False,True]).head(top_slider)
        fig = px.bar(aux, x='Restaurant Name', y=coluna, labels = { 'Restaurant Name' : 'Restaurante', coluna : nome_y},hover_data=[coluna],color=coluna,text=coluna) 
    
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

# VISÃO CUSINHA

# ============= IMPORTANDO DF E LIMPANDO DF ================

df = pd.read_csv('zomato.csv')

df1 = limpando_df( df )

# ======================== FIM =============================

# =================== BARRA LATERAL ========================

st.header('🍽️ Visão Restaurantes e Tipos de Culinária')
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

cuisines_opions = st.sidebar.multiselect(
    'Escolha os Tipos de Culinária :',
    ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
       'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
       'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
       'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
       'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç'],
    default = ['Italian','Brazilian', 'BBQ', 'Japanese', 'Home-made', 'American','French'])

st.sidebar.markdown("""___""")



st.sidebar.markdown('### Powered by Bruno Henrique')

# Linkando o  Filtro de país 
linhas_selecionadas = df1['nome_pais'].isin(countries_opions)
df1 = df1.loc[linhas_selecionadas,:]

# Linkando o  Filtro de país 
linhas_selecionadas = df1['Cuisines'].isin(cuisines_opions)
df1 = df1.loc[linhas_selecionadas,:]


# ======================== FIM =============================

# ====================== LAYOUT GRÁFICOS ==================
tab1, tab2 = st.tabs(['Tipo de Culinária','Restaurantes'])

with tab1:
    with st.container():
        fig = calc_cuisines(df1, coluna = 'Aggregate rating', name_y = 'Média Avaliação', filtro_entregas = 0)   
        fig.update_layout(title_text=f'Top {top_slider} Tipos de Culinária com maior média de avaliação', title_x=0.1)
        st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
        st.markdown("""___""")
               
    with st.container():
        col1, col2, = st.columns(2)
        
        with col1:
            fig = calc_cuisines(df1, coluna = 'Aggregate rating', name_y = 'Maior Avaliação', filtro_entregas = 0)      
            fig.update_layout(title_text=f'Top {top_slider} Tipos de Culinária com maior nota de avaliação', title_x=0.1)
            st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
            st.markdown("""___""")
            
        with col2:
            fig = calc_cuisines(df1, coluna = 'Restaurant ID', name_y = 'Quantidade de Tipos de Culinária', filtro_entregas = 1)       
            fig.update_layout(title_text=f'Top {top_slider} Tipos de Culinária que aceitam pedidos Online e fazem entrega', title_x=0.1)
            st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
            st.markdown("""___""")  
        
with tab2:
    with st.container():
        fig = calc_restaurantes(df1, coluna = 'Aggregate rating', filtro = 0, nome_y = 'Média Avaliação' )    
        fig.update_layout(title_text=f'Top 10 Restaurantes com maior média de avaliação', title_x=0.1)
        st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
        st.markdown("""___""")
        
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            fig = calc_restaurantes(df1, coluna = 'Votes', filtro = 1, nome_y = 'Quantidade de Avaliações' )       
            fig.update_layout(title_text=f'Top {top_slider} Restaurante com o maior número de Avaliações', title_x=0.1)
            st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
            st.markdown("""___""")
            
        with col2:
            fig = calc_restaurantes(df1, coluna = 'Average Cost for two', filtro = 1, nome_y = 'Maior valor para prato para 2' )       
            fig.update_layout(title_text=f'Top {top_slider} Restaurante com o maior valor de uma prato para duas pessoas', title_x=0.1)
            st.plotly_chart(fig, use_container_width = True) # Comando para plotar o grafico no streamlit
            st.markdown("""___""")
            