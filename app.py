import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Análise de Vendas com Insights Automáticos", layout="wide")
st.title("📊 Análise de Vendas com Insights Automáticos")

# Função para gerar modelo de planilha
@st.cache_data
def gerar_modelo_planilha():
    dados_exemplo = {
        "data da venda": ["2024-07-01"] * 30,
        "produto": ["Café", "Pão francês", "Croissant", "Bolo de cenoura", "Pão de queijo"] * 6,
        "quantidade": [10, 20, 15, 5, 12] * 6,
        "valor unitário": [5.0, 1.0, 3.5, 4.0, 2.5] * 6,
        "filial": ["Centro", "Centro", "Bairro", "Centro", "Bairro"] * 6,
        "total": [50.0, 20.0, 52.5, 20.0, 30.0] * 6,
    }
    df_exemplo = pd.DataFrame(dados_exemplo)
    buffer = BytesIO()
    df_exemplo.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

st.download_button(
    label="📄 Baixar modelo de planilha",
    data=gerar_modelo_planilha(),
    file_name="modelo_planilha_vendas.csv",
    mime="text/csv"
)

st.write("Faça upload da sua planilha de vendas (CSV ou Excel):")

arquivo = st.file_uploader("", type=["csv", "xlsx"])

if arquivo:
    try:
        if arquivo.name.endswith(".csv"):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)

        st.success("Arquivo carregado com sucesso!")

        # Verifica colunas obrigatórias
        colunas_esperadas = ["data da venda", "produto", "quantidade", "valor unitário", "filial", "total"]
        if all(col in df.columns for col in colunas_esperadas):
            df["data da venda"] = pd.to_datetime(df["data da venda"], errors='coerce')

            st.subheader("📊 Visualização Personalizada")
            col1, col2 = st.columns(2)
            with col1:
                eixo_x = st.selectbox("Escolha o eixo X:", options=df.columns)
            with col2:
                eixo_y = st.selectbox("Escolha o eixo Y:", options=df.select_dtypes(include=['number']).columns)

            if eixo_x and eixo_y:
                st.subheader("📈 Gráfico de Barras")
                dados_grafico = df.groupby(eixo_x)[eixo_y].sum().sort_values()
                fig, ax = plt.subplots()
                dados_grafico.plot(kind="barh", ax=ax)
                ax.set_xlabel(eixo_y)
                ax.set_ylabel(eixo_x)
                ax.set_title(f"{eixo_y} por {eixo_x}")
                st.pyplot(fig)

            st.subheader("💡 Insights Automáticos")
            vendas_produto = df.groupby("produto")["total"].sum()
            produto_top = vendas_produto.idxmax()
            valor_top = vendas_produto.max()
            produto_low = vendas_produto.idxmin()
            valor_low = vendas_produto.min()
            total_geral = df["total"].sum()
            media_diaria = df.groupby("data da venda")["total"].sum().mean()

            st.markdown(f"- 🥇 Produto mais vendido: **{produto_top}** (R$ {valor_top:.2f})")
            st.markdown(f"- 🧊 Produto com menor venda: **{produto_low}** (R$ {valor_low:.2f})")
            st.markdown(f"- 💰 Total geral vendido: **R$ {total_geral:.2f}**")
            st.markdown(f"- 📅 Média de vendas por dia: **R$ {media_diaria:.2f}**")

        else:
            st.error("A planilha deve conter as colunas: data da venda, produto, quantidade, valor unitário, filial, total")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
