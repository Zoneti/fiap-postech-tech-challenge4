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

# FILTRO LATERAL DE ANO, CONTINENTE E PAISES
st.sidebar.subheader('Parâmetros:')

input_tempo_experiencia = float(st.sidebar.slider('Selecione a quantidade de dias para a projeção:', 0,30))
st.write('Dias para projeção: ',input_tempo_experiencia)
col1, col2 = st.columns(2)
fig_preco = px.line(df, x="Data", y="Preco",  title="Preço do petróleo")


def predict_Prophet(df, modelo, periodo):
    pred = pd.DataFrame(columns=['ds', 'y'])

    start_date = (df.ds.max() + pd.DateOffset(1)).to_pydatetime()
    pred_dates = pd.date_range(start=start_date, periods=periodo, freq='D')
    pred_df = pd.DataFrame(pred_dates, columns=['ds'])
    forecast = modelo.predict(pred_df)
    pred[['ds', 'y']] = forecast[['ds', 'yhat']]

    return pred

def plotly_prev (ori, pred):
    fig = go.Figure()
    
    ori = ori[ori['ds'] >= pd.to_datetime('04-01-2024')]
    
    fig.add_trace(
        go.Scatter(x=ori.ds, y=ori.y,name='Valor Original')
        
    )
    fig.add_trace(
            go.Scatter(x=pred.ds, y=pred.y,name='Valor Previsto')
            
        )

    fig.update_layout(
        title='Projeção de Preço - Barril de Petróleo',
        xaxis_title='Data',
        yaxis_title='Preço US$'
    )
    
    return fig
#Predições 
if st.sidebar.button('Projetar'):
    df.columns = ['ds', 'y']
    with open('prophet_model.pkl', 'rb') as f:
        prophet_model = pickle.load(f)
    
    previsao = predict_Prophet(df, prophet_model, input_tempo_experiencia)
    
    col1.plotly_chart(plotly_prev(df, previsao), use_container_width=True)
    with col2:
        st.text('Lista de preços Projetados')
        previsao.columns = ['Data', 'Preco']
        previsao
else:
    col1.plotly_chart(fig_preco, use_container_width=True)