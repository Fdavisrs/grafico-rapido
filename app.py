import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Gráfico Rápido com GPT", layout="wide")

st.title("📊 Gráfico Rápido com GPT")
st.caption("Envie sua planilha (.csv ou .xlsx)")

uploaded_file = st.file_uploader("Drag and drop file here", type=["csv", "xlsx"])

if uploaded_file:
    # Carregar o arquivo
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Arquivo carregado com sucesso!")
    st.write("Visualização inicial dos dados:", df.head())

    # Remover colunas Unnamed
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Conversão de datas, se houver coluna 'data'
    if "data" in df.columns:
        try:
            df["data"] = pd.to_datetime(df["data"])
        except:
            pass

    # Escolher eixos
    col1, col2 = st.columns(2)
    with col1:
        eixo_x = st.selectbox("Escolha o eixo X (categoria):", df.columns)
    with col2:
        colunas_numericas = df.select_dtypes(include=["int", "float"]).columns
        eixo_y = st.selectbox("Escolha o eixo Y (valor numérico):", colunas_numericas)

    # Tipo de gráfico
    tipo = st.radio("Tipo de gráfico:", ["Barras", "Linha", "Pizza"])

    if eixo_x and eixo_y:
        agrupado = df.groupby(eixo_x)[eixo_y].sum().reset_index()

        st.subheader("Visualização do gráfico")

        fig, ax = plt.subplots(figsize=(10, 5))

        if tipo == "Barras":
            ax.bar(agrupado[eixo_x], agrupado[eixo_y], color="skyblue")
            ax.set_xlabel(eixo_x)
            ax.set_ylabel(eixo_y)
            ax.set_title(f"{eixo_y} por {eixo_x}")

        elif tipo == "Linha":
            ax.plot(agrupado[eixo_x], agrupado[eixo_y], marker="o", linestyle="-")
            ax.set_xlabel(eixo_x)
            ax.set_ylabel(eixo_y)
            ax.set_title(f"{eixo_y} por {eixo_x}")

        elif tipo == "Pizza":
            ax.pie(agrupado[eixo_y], labels=agrupado[eixo_x], autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            ax.set_title(f"{eixo_y} por {eixo_x}")

        st.pyplot(fig)
