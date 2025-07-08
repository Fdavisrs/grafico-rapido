import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gráfico Rápido", layout="centered")

st.title("📊 Gráfico Rápido")
st.subheader("Transforme sua planilha em gráficos")

uploaded_file = st.file_uploader("Envie sua planilha .CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📄 Dados carregados:")
    st.dataframe(df)

    colunas_disponiveis = df.columns.tolist()
    col_x = st.selectbox("Escolha a coluna para o eixo X", colunas_disponiveis)
    col_y = st.selectbox("Escolha a coluna para o eixo Y", colunas_disponiveis)

    if col_x == col_y:
        st.warning("❗ Selecione colunas diferentes para X e Y.")
    else:
        tipo = st.radio("Tipo de gráfico", ["Barras", "Linha", "Pizza"], horizontal=True)

        dados = df.groupby(col_x)[col_y].sum().reset_index()

        if tipo == "Barras":
            fig = px.bar(dados, x=col_x, y=col_y, text=col_y)
        elif tipo == "Linha":
            fig = px.line(dados, x=col_x, y=col_y, markers=True)
        else:
            fig = px.pie(dados, names=col_x, values=col_y)

        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Faça o upload de um arquivo CSV para começar.")
