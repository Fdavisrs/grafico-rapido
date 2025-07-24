import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Gráfico Mensal - Padaria", layout="wide")

st.title("🥖 Painel de Vendas por Mês")
st.caption("Envie sua planilha de vendas (.csv ou .xlsx)")

uploaded_file = st.file_uploader("Arraste aqui o arquivo", type=["csv", "xlsx"])

if uploaded_file:
    # Carrega o arquivo
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Remove colunas automáticas
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Garante que a coluna "data" está no formato datetime
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Cria coluna de mês/ano
    df["mes"] = df["data"].dt.strftime("%Y-%m")

    st.success("Arquivo carregado com sucesso!")
    st.write("Visualização inicial dos dados:", df.head())

    # Filtro de mês
    meses_disponiveis = sorted(df["mes"].dropna().unique())
    mes_selecionado = st.selectbox("Selecione o mês para análise:", meses_disponiveis)

    # Filtra dados do mês selecionado
    df_mes = df[df["mes"] == mes_selecionado]

    # Mostra resumo
    st.markdown(f"### 📅 Dados de {mes_selecionado}")
    st.dataframe(df_mes)

    # Seleção de eixo Y
    colunas_numericas = df_mes.select_dtypes(include=["int", "float"]).columns.tolist()
    eixo_y = st.selectbox("Escolha o dado numérico para o gráfico (eixo Y):", colunas_numericas)

    # Eixo X fixo: produto
    eixo_x = "produto"
    tipo = st.radio("Tipo de gráfico:", ["Barras", "Linha", "Pizza"])

    # Agrupa os dados
    agrupado = df_mes.groupby(eixo_x)[eixo_y].sum().reset_index()

    st.markdown(f"### 📊 Gráfico de {eixo_y} por produto")

    fig, ax = plt.subplots(figsize=(10, 5))

    if tipo == "Barras":
        ax.bar(agrupado[eixo_x], agrupado[eixo_y], color="orange")
        ax.set_ylabel(eixo_y)
        ax.set_xlabel("Produto")
        ax.set_title(f"{eixo_y} por produto - {mes_selecionado}")
        plt.xticks(rotation=45)

    elif tipo == "Linha":
        ax.plot(agrupado[eixo_x], agrupado[eixo_y], marker="o")
        ax.set_ylabel(eixo_y)
        ax.set_xlabel("Produto")
        ax.set_title(f"{eixo_y} por produto - {mes_selecionado}")
        plt.xticks(rotation=45)

    elif tipo == "Pizza":
        ax.pie(agrupado[eixo_y], labels=agrupado[eixo_x], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        ax.set_title(f"{eixo_y} por produto - {mes_selecionado}")

    st.pyplot(fig)
