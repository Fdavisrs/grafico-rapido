import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Gráfico Rápido com CSV", layout="wide")

# Título do app
st.title("📊 Gerador de Gráficos a partir de Planilhas CSV")

# Link para download do modelo de planilha
with open("modelo_planilha_vendas.csv", "rb") as file:
    st.download_button(
        label="📥 Baixar modelo de planilha",
        data=file,
        file_name="modelo_planilha_vendas.csv",
        mime="text/csv"
    )

# Upload do arquivo
uploaded_file = st.file_uploader("Faça o upload da sua planilha CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Planilha carregada com sucesso!")
        st.dataframe(df)

        # Seleção de colunas para os eixos
        st.subheader("Selecione os dados para o gráfico")

        colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
        colunas_categoricas = df.select_dtypes(include=["object"]).columns.tolist()

        eixo_x = st.selectbox("Eixo X (categoria)", colunas_categoricas)
        eixo_y = st.selectbox("Eixo Y (valor numérico)", colunas_numericas)

        tipo_grafico = st.radio("Tipo de gráfico", ["Barra", "Linha", "Pizza"])

        if eixo_x and eixo_y:
            dados_agrupados = df.groupby(eixo_x)[eixo_y].sum().sort_values(ascending=False)

            st.subheader("Gráfico gerado:")

            fig, ax = plt.subplots(figsize=(10, 6))

            if tipo_grafico == "Barra":
                dados_agrupados.plot(kind="bar", ax=ax)
                ax.set_ylabel(eixo_y)
                ax.set_xlabel(eixo_x)
                ax.set_title(f"{eixo_y} por {eixo_x}")

            elif tipo_grafico == "Linha":
                dados_agrupados.plot(kind="line", marker='o', ax=ax)
                ax.set_ylabel(eixo_y)
                ax.set_xlabel(eixo_x)
                ax.set_title(f"{eixo_y} por {eixo_x}")

            elif tipo_grafico == "Pizza":
                dados_agrupados.plot(kind="pie", autopct='%1.1f%%', ax=ax)
                ax.set_ylabel("")
                ax.set_title(f"{eixo_y} por {eixo_x}")

            st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
