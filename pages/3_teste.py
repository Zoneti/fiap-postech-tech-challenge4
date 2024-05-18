import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregue um DataFrame de exemplo com algumas opções
data = {'opcao1': ['A', 'B', 'C'],
        'opcao2': ['X', 'Y', 'Z']}
df = pd.DataFrame(data)

# Crie três filtros
filtro1 = st.selectbox('Selecione a opção 1:', df['opcao1'])
filtro2 = st.selectbox('Selecione a opção 2:', df['opcao2'])
filtro3 = st.slider('Selecione um valor:', 0, 10, 5)

# Exiba as opções selecionadas
st.write('Opção 1 selecionada:', filtro1)
st.write('Opção 2 selecionada:', filtro2)
st.write('Valor selecionado:', filtro3)

# Crie um gráfico de barras simples
plt.bar(['A', 'B', 'C'], [3, 5, 2])
st.pyplot(plt)