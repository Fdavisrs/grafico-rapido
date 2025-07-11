import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata

st.set_page_config(page_title="Gráfico Rápido", layout="wide")

st.title("📊 Gráfico Rápido")
st.markdown("Envie sua planilha CSV")

# Função "agente inteligente" para padronizar colunas
def padronizar_nome_coluna(col):
    col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')  # remove acentos
    col = col.lower().strip().replace(" ", "_")  # minúsculas e underline
    return col

# Upload
file = st.file_uploader("Arraste ou selecione o arquivo CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file, sep=None, engine="python")

    # Normaliza nomes de colunas
    df.columns = [padronizar_nome_coluna(col) for col in df.columns]

    # Remove colunas totalmente vazias ou sem sentido
    df.dropna(axis=1, how='all', inplace=True)
    df = df.loc[:, ~df.columns.str.contains("unnamed")]

    st.subheader("📋 Pré-visualização dos dados")
    st.dataframe(df.head(), use_container_width=True)

    colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    colunas_disponiveis = df.columns.tolist()

    if colunas_numericas and colunas_disponiveis:
        st.subheader("🎯 Escolha os eixos do gráfico")
        col_x = st.selectbox("Eixo X", colunas_disponiveis)
        col_y = st.selectbox("Eixo Y (somente colunas numéricas)", colunas_numericas)

        if col_x != col_y:
            dados = df.groupby(col_x)[col_y].sum().reset_index()

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(dados[col_x].astype(str), dados[col_y])
            ax.set_xlabel(col_x)
            ax.set_ylabel(col_y)
            ax.set_title(f"{col_y} por {col_x}")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.warning("❗ Selecione colunas diferentes para os eixos X e Y.")
    else:
        st.error("❌ Não foram encontradas colunas numéricas para gerar o gráfico.")
