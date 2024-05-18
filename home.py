import streamlit as st
import pandas as pd
import plotly.express as px

st.header('Dashboard Produção de Petróleo - IPEA')

# BREVE TRATAMENTO DA BASE
df_producao = pd.read_csv("bases\data_ext\df_producao_petroleo_T.csv", sep=";", decimal=".")
df_producao["Data"] = pd.to_datetime(df_producao['Data'])
df_producao = df_producao.set_index(df_producao['Data'])
df_producao['Mes-Ano'] = df_producao['Data'].apply(lambda x: str(x.month) + '-' + str(x.year))
df_producao['Mes'] = df_producao['Data'].dt.strftime('%B')
df_producao['Ano'] = df_producao['Data'].dt.year
df_paises = df_producao.drop(["Data", "Ano", "Mes", "Mes-Ano"], axis = 1 ).columns


# FILTRO LATERAL DE ANO E PAISES


st.sidebar.subheader('Filtros:')
fAno = st.sidebar.multiselect(
        "Selecione um ou mais Anos:", 
        options=df_producao['Ano'].unique(),
        default=df_producao['Ano'].unique()
    )

fPaises = st.sidebar.multiselect(
        'Selecione um ou mais paises:',
        options=df_paises
    )

df_filtered = df_producao.loc[
        df_producao['Data'].dt.year.isin(fAno)]

df_filtered = df_producao.query(
    "Ano == @fAno"
)


st.dataframe(df_filtered)



#pd.melt(df_prod.reset_index(), id_vars=['produto'], var_name='ano', value_name='valor').sort_values(['produto'], ascending=False)
















#ano_selecionado = st.sidebar.multiselect('Selecione um ou mais anos:', df_producao['Ano'].unique())
#df_f_ano = df_producao[df_producao['Data'].dt.year.isin(ano_selecionado)]


#colunas_selecionada = st.sidebar.multiselect('Selecione um ou mais paises:', df_paises)
#df_f_cols = df_producao.columns.isin(df_paises)

#df_producao



#col1, col2 = st.columns(2)
#col3, col4, col5 = st.columns(3)

#fig_date = px.bar(df_filtered, x=df_filtered.index, y=df_filtered.columns, title="Produção de petroleo Mundial")
#col1.plotly_chart(fig_date)











#if st.sidebar.checkbox('Mostre o Dataframe'):
#    df_filtered






