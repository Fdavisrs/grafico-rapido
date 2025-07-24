import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Análise de Vendas com Insights Automáticos", layout="wide")
st.title("\U0001f4ca Análise de Vendas com Insights Automáticos")

# Botão para baixar o modelo de planilha
with open("modelo_planilha_vendas.csv", "rb") as file:
    st.download_button(
        label="📄 Baixar modelo de planilha",
        data=file,
        file_name="modelo_planilha_vendas.csv",
        mime="text/csv"
    )

st.markdown("Faça upload da sua planilha de vendas (CSV ou Excel):")
uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Limpeza de colunas: tira acentos, deixa minúsculo, tira espaços
        df.columns = df.columns.str.strip().str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

        # Colunas obrigatórias
        required_columns = ["data da venda", "produto", "quantidade", "valor unitario", "filial", "total"]
        if not all(col in df.columns for col in required_columns):
            st.error("A planilha deve conter as colunas: data da venda, produto, quantidade, valor unitario, filial, total")
        else:
            # Conversões
            df["data da venda"] = pd.to_datetime(df["data da venda"], errors='coerce')
            df = df.dropna(subset=["data da venda"])  # remove linhas com datas inválidas

            st.success("Arquivo carregado com sucesso!")

            # Gráficos de análise
            st.subheader("Gráfico de Vendas por Produto")
            produto_agrupado = df.groupby("produto")["total"].sum().sort_values(ascending=False)
            fig1, ax1 = plt.subplots()
            produto_agrupado.plot(kind='bar', ax=ax1)
            ax1.set_ylabel("Total de Vendas (R$)")
            ax1.set_title("Total de Vendas por Produto")
            st.pyplot(fig1)

            st.subheader("Gráfico de Vendas por Filial")
            filial_agrupado = df.groupby("filial")["total"].sum().sort_values(ascending=False)
            fig2, ax2 = plt.subplots()
            filial_agrupado.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
            ax2.set_ylabel("")
            ax2.set_title("Participação de Vendas por Filial")
            st.pyplot(fig2)

            # Insights automatizados
            st.subheader("\U0001f4a1 Insights de Vendas")
            melhor_dia = df.groupby("data da venda")["total"].sum().idxmax().strftime('%d/%m/%Y')
            produto_top = produto_agrupado.idxmax()
            filial_top = filial_agrupado.idxmax()

            st.markdown(f"- **Melhor dia de vendas:** {melhor_dia}")
            st.markdown(f"- **Produto mais vendido (R$):** {produto_top}")
            st.markdown(f"- **Filial com maior faturamento:** {filial_top}")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
