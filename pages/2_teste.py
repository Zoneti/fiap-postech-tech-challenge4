import pandas as pd
import streamlit as st

# Exemplo de dados fictícios
data = {
    'Animal Type': ['Dog', 'Cat', 'Spider'],
    'Breed': ['bulldog', 'asky', 'asky'],
    'Color': ['brown', 'yellow', 'black']
}

df = pd.DataFrame(data)

# Filtros multiselect independentes
options1 = st.multiselect('Animal Type', df['Animal Type'].unique())
options2 = st.multiselect('Breed', df['Breed'].unique())
options3 = st.multiselect('Color', df['Color'].unique())

# Filtrando o DataFrame com base nas seleções
filtered_df = df[
    (df['Animal Type'].isin(options1) | (len(options1) == 0)) &
    (df['Breed'].isin(options2) | (len(options2) == 0)) &
    (df['Color'].isin(options3) | (len(options3) == 0))
]

# Exibindo o DataFrame filtrado
st.write(filtered_df)