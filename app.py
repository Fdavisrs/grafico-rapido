import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata

# Configuração da página
st.set_page_config(page_title="Gráfico Rápido", layout="wide")
st.title("📊 Gráfico Rápido")
st.markdown("Envie sua planilha CSV")

# Padroniza os nomes das colunas
def padronizar_nome_coluna(col):
    col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')
    return col.lower().strip().replace(" ", "_")

# Colunas irrelevantes para análise
colunas_ignoradas = [
    "cpf", "cnpj", "telefone", "celular", "email", "nome", "id", "codigo", "nota", "endereco", "numero_nota", "serie", "nfe"
]

# Detecta colunas numéricas úteis com base no nome e tipo
def colunas_metricas(df):
    metricas_comuns = ["valor", "quantidade", "preco", "total", "custo", "lucro", "vendas", "desconto"]
    colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
    return [col for col in colunas_numericas if any(m in col for m in metricas_comuns)]

# Upload do arquivo
file = st.file_uploader("Arraste ou selecione o arquivo CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file, sep=None, engine="python")

    # Padroniza colunas
    df.columns = [padronizar_nome_coluna(col) for col in df.columns]
    df.dropna(axis=1, how='all', inplace=True)
    df = df.loc[:, ~df.columns.str.contains("unnamed")]

    st.subheader("📋 Pré-visualização dos dados")
    st.dataframe(df.head(), use_container_width=True)

    # Detecta colunas úteis
    colunas_x_validas = [
        col for col in df.select_dtypes(include='object').columns
        if not any(ign in col for ign in colunas_ignoradas)
    ]
    colunas_y_validas = colunas_metricas(df)

    if not colunas_x_validas or not colunas_y_validas:
        st.error("❌ Não foi possível identificar colunas relevantes para análise.")
    else:
        eixo_x = st.selectbox("Escolha a coluna para o eixo X", colunas_x_validas)
        eixo_y = st.selectbox("Escolha a coluna para o eixo Y (somente numérica)", colunas_y_validas)

        if eixo_x != eixo_y:
            st.subheader("📈 Resultado")
            fig, ax = plt.subplots(figsize=(12, 6))
            df.groupby(eixo_x)[eixo_y].sum().sort_values(ascending=False).plot(kind="bar", ax=ax)
            ax.set_xlabel(eixo_x)
            ax.set_ylabel(eixo_y)
            ax.set_title(f"{eixo_y} por {eixo_x}")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("⚠️ Selecione colunas diferentes para X e Y.")
