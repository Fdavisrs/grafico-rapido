import streamlit as st
import pandas as pd

st.title("📊 Visualizador de Vendas - Versão com Mapeamento Dinâmico")

file = st.file_uploader("📁 Envie sua planilha CSV", type=["csv"])

if file is not None:
    try:
        # Tenta abrir com vírgula, se falhar tenta com ponto e vírgula
        try:
            df = pd.read_csv(file)
        except:
            df = pd.read_csv(file, sep=';')

        st.success("✅ Planilha carregada com sucesso!")
        st.dataframe(df.head())

        st.subheader("🧩 Mapeamento de Colunas")
        col_data = st.selectbox("🗓️ Qual é a coluna de **data da venda**?", df.columns)
        col_produto = st.selectbox("📦 Qual é a coluna de **produto**?", df.columns)
        col_valor = st.selectbox("💰 Qual é a coluna de **valor da venda**?", df.columns)

        # Converter a coluna de data
        df[col_data] = pd.to_datetime(df[col_data], errors='coerce')

        st.markdown("---")

        st.subheader("📉 Vendas por Produto")
        vendas_por_produto = df.groupby(col_produto)[col_valor].sum().sort_values(ascending=False)
        st.bar_chart(vendas_por_produto)

        st.subheader("📈 Vendas ao Longo do Tempo")
        vendas_por_data = df.groupby(col_data)[col_valor].sum().sort_index()
        st.line_chart(vendas_por_data)

    except Exception
