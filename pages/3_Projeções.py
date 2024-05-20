import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from prophet import Prophet

st.set_page_config(layout='wide')

st.header('Projeções do Preço do Petróleo')
st.text('É feita uma projeção em um algoritimo de ML com base nos dias selecionado no campo de filtro.')

df = pd.read_csv("bases/modelo/df_modelo.csv", sep=";", decimal=".")
df["Data"] = pd.to_datetime(df['Data'])
#df = df.groupby(['Data']).sum()

df['Ano'] = df['Data'].dt.year


# FILTRO LATERAL DE ANO, CONTINENTE E PAISES
st.sidebar.subheader('Filtros:')
fAno = st.sidebar.multiselect(
        "Selecione um ou mais Anos:", 
        options=df['Ano'].sort_values().unique()
        #,default=2023
    )
filtered_df = df[
    (df['Ano'].isin(fAno) | (len(fAno) == 0)) ]

input_tempo_experiencia = float(st.sidebar.slider('Selecione a quantidade de dias para a projeção:', 0,30))
input_tempo_experiencia
col1, col2 = st.columns(2)
fig_preco = px.line(filtered_df, x="Data", y="Preco",  title="Preço do petróleo")
col1.plotly_chart(fig_preco, use_container_width=True)

#Predições 
if st.button('Projetar'):
    with open('../prophet_model.pkl', 'rb') as f:
        prophet_model = pickle.load(f)