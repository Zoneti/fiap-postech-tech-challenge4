import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

st.header('Variação do Preço do Petróleo')
st.subheader('Variação com base nos eventos globais')

df = pd.read_csv("bases\data_ext\df_preco_barril_eventos.csv", sep=";", decimal=".")
df["Data"] = pd.to_datetime(df['Data'])


# FILTRO LATERAL DE ANO, CONTINENTE E PAISES
st.sidebar.subheader('Filtros:')

fAno = st.sidebar.multiselect(
        'Selecione um ou mais anos:',
        options=df['Ano'].unique()
        #,default=df_producao['Continent'].unique()
    )

fEvents = st.sidebar.multiselect(
        'Selecione um ou mais continentes:',
        options=df['Eventos'].unique()
        #,default=df_producao['Continent'].unique()
    )

filtered_df = df[
    (df['Ano'].isin(fAno) | (len(fAno) == 0)) &
    (df['Eventos'].isin(fEvents) | (len(fEvents) == 0))]

# DIVISAO DOS 2 SETORES DA METADE DE CIMA DA PAGINA DO STREAMLIT
col1, col2 = st.columns(2)

df_ano = filtered_df.groupby(['Ano'])['Preco'].sum().reset_index()
fig_preco = px.line(df_ano, x="Ano", y="Preco", markers=True, title="Preço do petróleo anual")
col1.plotly_chart(fig_preco, use_container_width=True)

df_events = filtered_df[['Ano','Eventos']]
df_events = df_events.drop_duplicates()
with col2:
    st.text('Lista de eventos mundiais')
    df_events



st.subheader('Base de dados.')

col3, col4 = st.columns(2)

filtered_df = filtered_df.groupby(['Data','Ano','Eventos']).sum()
filtered_df
