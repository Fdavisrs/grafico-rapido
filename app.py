import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Painel de Vendas por Mês")

st.title("🥖 Painel de Vendas por Mês")

st.markdown("Envie sua planilha de vendas (.csv ou .xlsx)")

uploaded_file = st.file_uploader("Arraste aqui o arquivo", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Ler CSV ou XLSX
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Corrigir nomes de colunas
    df.columns = df.columns.str.lower().str.strip()
    if "unnamed: 0" in df.columns:
        df = df.drop(columns=["unnamed: 0"])

    # Adiciona uma coluna de mês fixa
    df["mes"] = "2024-11"

    # Visualização dos dados
    st.subheader("📄 Prévia dos Dados")
    st.dataframe(df.head())

    # Seleção de variáveis
    col1, col2, col3 = st.columns(3)

    with col1:
        eixo_x = st.selectbox("Escolha o eixo X (agrupamento):", df.columns)

    with col2:
        colunas_numericas = df.select_dtypes(include='number').columns.tolist()
        eixo_y = st.selectbox("Escolha o eixo Y (valor numérico):", colunas_numericas)

    with col3:
        tipo_grafico = st.selectbox("Tipo de gráfico:", ["Barra", "Linha", "Pizza"])

    if eixo_x and eixo_y:
        agrupado = df.groupby(eixo_x)[eixo_y].sum().sort_values(ascending=False)

        st.subheader(f"📊 Gráfico de {eixo_y} por {eixo_x}")
        fig, ax = plt.subplots()

        if tipo_grafico == "Barra":
            agrupado.plot(kind="bar", ax=ax)
        elif tipo_grafico == "Linha":
            agrupado.plot(kind="line", ax=ax, marker="o")
        elif tipo_grafico == "Pizza":
            agrupado.plot(kind="pie", ax=ax, autopct="%1.1f%%", ylabel="")

        st.pyplot(fig)
