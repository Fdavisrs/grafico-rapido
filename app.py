import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Gráfico Rápido")

uploaded_file = st.file_uploader("Envie sua planilha CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Pré-visualização dos dados:")
    st.dataframe(df)

    coluna_x = st.selectbox("Escolha a coluna X", df.columns)
    coluna_y = st.selectbox("Escolha a coluna Y", df.columns)

    fig = px.bar(df, x=coluna_x, y=coluna_y)
    st.plotly_chart(fig)
