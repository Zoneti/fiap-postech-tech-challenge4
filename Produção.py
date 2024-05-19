import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

st.header('Produção de Petróleo - IPEA')
st.subheader('Produção Mundial em Barris dos Ultimos 20 Anos.')

# BREVE TRATAMENTO DA BASE GERAL
df_producao = pd.read_csv("bases\data_ext\df_producao_petroleo_dash.csv", sep=";", decimal=".")
df_producao = df_producao.loc[df_producao['Continent'] != 'World']
df_producao["Mês"] = pd.to_datetime(df_producao['Mês'])
df_producao = df_producao.set_index(df_producao['Mês'])
df_producao['Mes'] = df_producao['Mês'].dt.strftime('%B')
df_producao['Ano'] = df_producao['Mês'].dt.year
df_producao = df_producao[df_producao['Ano'] >= 2004]

# CRIACAO DO DF MUNDIAL
df_agrupado_cont = df_producao.groupby(['Ano', 'Continent'])['Quantidade'].sum().reset_index()

# DIVISAO DOS 2 SETORES DA METADE DE CIMA DA PAGINA DO STREAMLIT
col1, col2 = st.columns(2)
fig_ano = px.bar(df_agrupado_cont, x='Ano', y='Quantidade', color='Continent', 
                color_discrete_map={
                "Europe": "yellow",
                "Asia": "violet",
                "North America": "lightblue",
                "South America": "lightgreen",
                "Oceania": "grey",
                "Africa": "goldenrod"},title="Produção de petróleo mundial")
col1.plotly_chart(fig_ano, use_container_width=True)

fig_conti = px.line(df_agrupado_cont, x="Ano", y="Quantidade", color='Continent', markers=True,
                color_discrete_map={
                "Europe": "yellow",
                "Asia": "violet",
                "North America": "lightblue",
                "South America": "lightgreen",
                "Oceania": "grey",
                "Africa": "goldenrod"}, title="Produção de petróleo mundial por continente")
col2.plotly_chart(fig_conti, use_container_width=True)


# DIVISAO DOS 3 SETORES DA METADE DE BAIXO DA PAGINA DO STREAMLIT
st.markdown("<hr>", unsafe_allow_html=True)

st.subheader('Produção Regional dos Ultimos 20 Anos.')

col3, col4 = st.columns(2)

# FILTRO LATERAL DE ANO, CONTINENTE E PAISES
st.sidebar.subheader('Filtros:')
fAno = st.sidebar.multiselect(
        "Selecione um ou mais Anos:", 
        options=df_producao['Ano'].sort_values().unique()
        #,default=2023
    )

fContinentes = st.sidebar.multiselect(
        'Selecione um ou mais continentes:',
        options=df_producao['Continent'].unique()
        #,default=df_producao['Continent'].unique()
    )

fPaises = st.sidebar.multiselect(
        'Selecione um ou mais paises:',
        options=df_producao['Country'].sort_values().unique()
        #,default='Brazil'
    )

filtered_df = df_producao[
    (df_producao['Ano'].isin(fAno) | (len(fAno) == 0)) &
    (df_producao['Continent'].isin(fContinentes) | (len(fContinentes) == 0)) &
    (df_producao['Country'].isin(fPaises) | (len(fPaises) == 0))]


filtered_df2 = filtered_df.groupby(['Ano', 'Continent', 'Country'])['Quantidade'].sum().reset_index()



# GRAFICOS DA SEGUNDA METADE DA PAGINA
df_agrupado_g = filtered_df2.groupby(filtered_df2['Country'])['Quantidade'].sum().reset_index()
df_agrupado_g = df_agrupado_g.sort_values('Quantidade',ascending=False)
df_top10 = df_agrupado_g.head(10)

fig_ranking = px.bar(df_top10, x='Quantidade', y='Country', title="Ranking de Produção de Petróleo Mundial",orientation='h')
col3.plotly_chart(fig_ranking, use_container_width=True)


if fContinentes:
    fig_pie_conti = px.pie(filtered_df2, names="Country", values="Quantidade",title="Produção de Petróleo Total do Continente Filtrado")
    col4.plotly_chart(fig_pie_conti, use_container_width=True)
else:
    fig_pie_conti = px.pie(filtered_df2, names="Continent", values="Quantidade", color='Continent',
                color_discrete_map={
                "Europe": "yellow",
                "Asia": "violet",
                "North America": "lightblue",
                "South America": "lightgreen",
                "Oceania": "grey",
                "Africa": "goldenrod"},title="Produção de Petróleo Total por Continente")
    col4.plotly_chart(fig_pie_conti, use_container_width=True)



col5, col6 = st.columns(2)

fig_conti_reg = px.line(filtered_df2, x="Ano", y="Quantidade", color='Country', markers=True, title="Produção de Petróleo Anual por Pais")
col5.plotly_chart(fig_conti_reg, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# SWITCH DE EXIBICAO DO DF
if st.checkbox('Mostre os Dados'):
    filtered_df
