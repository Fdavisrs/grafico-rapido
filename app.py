import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata

# Configuração da página
st.set_page_config(page_title="Gráfico Rápido", layout="wide")
st.title("📊 Gráfico Rápido")
st.markdown("Envie sua planilha CSV")

# 🔤 Padroniza os nomes das colunas
def padronizar_nome_coluna(col):
    col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')
    col = col.lower().strip().replace(" ", "_")
    return col

# 🧹 Remove colunas irrelevantes
colunas_ignoradas = [
    "cpf", "cnpj", "telefone", "celular", "numero_da_nota", "nota_fiscal",
    "codigo_cliente", "id", "email", "nome", "endereco"
]

# ✅ NOVO: pega todas as colunas numéricas (sem filtrar por nome)
def colunas_metricas(df):
    return df.select_dtypes(include=['float64', 'int64']).columns.tolist()

# ⬆️ Upload do arquivo
file = st.file_uploader("Arraste ou selecione o arquivo CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file, sep=None, engine="python")

    # Padroniza os nomes das colunas
    df.columns = [padronizar_nome_coluna(col) for col in df.columns]
    df.dropna(axis=1, how='all', inplace=True)
    df = df.loc[:, ~df.columns.str.contains("unnamed")]

    # 📋 Mostra os dados
    st.subheader("📋 Pré-visualização dos dados")
    st.dataframe(df.head(), use_container_width=True)

    # Filtra colunas
    colunas_validas = [col for col in df.columns if col not in colunas_ignoradas]
    colunas_metricas_validas = colunas_metricas(df)

    if len(colunas_validas) == 0 or len(colunas_metricas_validas) == 0:
        st.error("❌ Não foi possível identificar colunas relevantes para análise.")
    else:
        # 🎯 Seleção de colunas
        eixo_x = st.selectbox("Escolha a coluna para o eixo X", colunas_validas)
        eixo_y = st.selectbox("Escolha a coluna para o eixo Y (somente numérica)", colunas_metricas_validas)

        if eixo_x != eixo_y:
            # 📊 Gera o gráfico
            st.subheader("📈 Resultado")
            fig, ax = plt.subplots()
            df.groupby(eixo_x)[eixo_y].sum().plot(kind="bar", ax=ax)
            ax.set_xlabel(eixo_x)
            ax.set_ylabel(eixo_y)
            ax.set_title(f"{eixo_y} por {eixo_x}")
            st.pyplot(fig)
        else:
            st.warning("⚠️ Selecione colunas diferentes para X e Y.")
