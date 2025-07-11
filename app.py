import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata

st.set_page_config(page_title="Gráfico Rápido", layout="wide")
st.title("📊 Gráfico Rápido")
st.markdown("Envie sua planilha CSV")

# Padroniza os nomes das colunas
def padronizar_nome_coluna(col):
    col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')
    col = col.lower().strip().replace(" ", "_")
    return col

# Define colunas irrelevantes para gráficos
colunas_ignoradas = [
    "cpf", "cnpj", "telefone", "celular", "numero_da_nota", "nota_fiscal", "codigo_cliente", "id", "codigo"
]

# Detecta colunas numéricas úteis com base no nome
def colunas_metricas(df):
    metricas_comuns = ["valor", "quantidade", "preco", "total", "custo", "lucro", "vendas", "desconto"]
    return [
        col for col in df.select_dtypes(include=['float64', 'int64']).columns
        if any(m in col for m in metricas_comuns)
    ]

# Upload
file = st.file_uploader("Arraste ou selecione o arquivo CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file, sep=None, engine="python")

    # Padroniza colunas
    df.columns = [padronizar_nome_coluna(col) for col in df.columns]
    df.dropna(axis=1, how='all', inplace=True)
    df = df.loc[:, ~df.columns.str.contains("unnamed")]

    st.subheader("📋 Pré-visualização dos dados")
    st.dataframe(df.head(), use_container_width=True)

    # Filtra colunas para análise
    colunas_validas = [col for col in df.columns if col not in colunas_ignoradas]
    colunas_numericas = colunas_metricas(df)
    
    if colunas_validas and colunas_numericas:
        st.subheader("🎯 Escolha os eixos do gráfico")
        col_x = st.selectbox("Eixo X", colunas_validas)
        col_y = st.selectbox("Eixo Y (somente colunas numéricas úteis)", colunas_numericas)

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
        st.error("❌ Não foi possível identificar colunas relevantes para análise.")
