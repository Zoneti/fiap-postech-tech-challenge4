import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
from prophet import Prophet
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

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

def predict_Prophet(df, modelo, periodo):
    pred = pd.DataFrame(columns=['ds', 'y'])

    start_date = (df.ds.max() + pd.DateOffset(1)).to_pydatetime()
    pred_dates = pd.date_range(start=start_date, periods=periodo, freq='D')
    pred_df = pd.DataFrame(pred_dates, columns=['ds'])
    forecast = modelo.predict(pred_df)
    pred[['ds', 'y']] = forecast[['ds', 'yhat']]

    return pred

def plot_prev (ori, pred, dateLimit=None, test=None):
    fig, ax = plt.subplots(figsize=(30,8))

    if dateLimit is not None:
        ori = ori[ori['ds'] >= pd.to_datetime(dateLimit)]

    sns.lineplot(ori, x='ds', y='y', ax=ax, label='Preço Barril', color='black')

    if test is not None:
        sns.lineplot(test, x='ds', y='y', ax=ax, color='blue', label='Valor Teste')

    sns.lineplot(pred, x='ds', y='y', ax=ax, color='red', label='Valor Previsto')


    ax.grid(True, color='black', linewidth=0.2, axis='y')

    ax.legend()

    ax.set_title('Previsão Preço Barril Petroleo', fontsize=15)
    ax.set_xlabel('')
    ax.set_ylabel('Preço Barril Petroleo')

    #plt.show()
    return fig

#Predições 
if st.button('Projetar'):
    with open('prophet_model.pkl', 'rb') as f:
        prophet_model = pickle.load(f)
    
    df1 = pd.read_csv("bases/modelo/df_modelo_10.csv", sep=";", parse_dates = [0], decimal=".")
    previsao = predict_Prophet(df1, prophet_model, input_tempo_experiencia)
    previsao
    st.pyplot(plot_prev(df1,previsao, '04-01-2024'))
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df1.ds, y=df1.y,name='Valor Original')
        
    )
    fig.add_trace(
            go.Scatter(x=previsao.ds, y=previsao.y,name='Valor Previsto')
            
        )

    fig.update_layout(
        title='Projeção de Preço - Barril de Petróleo',
        xaxis_title='Data',
        yaxis_title='Preço US$'
    )
    st.plotly_chart(fig)