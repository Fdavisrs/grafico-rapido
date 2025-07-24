import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Função para gerar modelo da planilha CSV
def gerar_modelo_planilha():
    colunas = ['data', 'produto', 'quantidade', 'valor_unitario', 'filial']
    df_modelo = pd.DataFrame(columns=colunas)
    df_modelo = df_modelo.reindex(range(30))  # 30 linhas em branco
    buffer = BytesIO()
    df_modelo.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

# Título
st.title("📊 Gerador de Gráficos a partir de Planilhas CSV")
st.write("Faça o upload da sua planilha CSV ou baixe o modelo para preencher.")

# Botão para baixar o modelo
buffer = gerar_modelo_planilha()
st.download_button(
    label="📥 Baixar modelo de planilha",
    data=buffer,
    file_name="modelo_planilha_vendas.csv",
    mime="text/csv"
)

# Upload da planilha
uploaded_file = st.file_uploader("Envie sua planilha", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Tentativa de conversão da coluna 'data' para datetime
        if "data" in df.columns:
            df["data"] = pd.to_datetime(df["data"], errors="coerce")

        st.subheader("Prévia dos dados")
        st.dataframe(df)

        colunas_numericas = df.select_dtypes(include="number").columns.tolist()
        colunas_categoricas = df.select_dtypes(exclude="number").columns.tolist()

        # Seleções
        eixo_x = st.selectbox("Escolha o eixo X (categorias):", colunas_categoricas)
        eixo_y = st.selectbox("Escolha o eixo Y (valor numérico):", colunas_numericas)
        tipo_grafico = st.radio("Tipo de gráfico:", ["Barra", "Pizza", "Linha"])

        # Geração do gráfico
        st.subheader("Gráfico gerado")

        if tipo_grafico == "Barra":
            df_grouped = df.groupby(eixo_x)[eixo_y].sum().sort_values(ascending=False)
            st.bar_chart(df_grouped)

        elif tipo_grafico == "Pizza":
            df_grouped = df.groupby(eixo_x)[eixo_y].sum()
            fig, ax = plt.subplots()
            ax.pie(df_grouped, labels=df_grouped.index, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)

        elif tipo_grafico == "Linha":
            df_grouped = df.groupby(eixo_x)[eixo_y].sum()
            st.line_chart(df_grouped)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar a planilha: {e}")
