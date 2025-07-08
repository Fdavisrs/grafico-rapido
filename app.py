import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gráfico Rápido", layout="centered")

st.title("📊 Gráfico Rápido")
st.subheader("Transforme sua planilha em gráficos automaticamente")

uploaded_file = st.file_uploader("Envie sua planilha .CSV com colunas como: Data, Produto, Categoria, Quantidade, Valor Unitário", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Verificação de colunas básicas
        colunas_necessarias = {"Data", "Produto", "Categoria", "Quantidade", "Valor Unitário"}
        if not colunas_necessarias.issubset(df.columns):
            st.error(f"❌ Sua planilha deve conter as colunas: {', '.join(colunas_necessarias)}")
        else:
            # Converter datas
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
            df = df.dropna(subset=["Data", "Produto", "Categoria", "Quantidade", "Valor Unitário"])

            # Calcular coluna Total
            df["Total"] = df["Quantidade"] * df["Valor Unitário"]

            st.success("✅ Planilha carregada com sucesso!")

            st.markdown("### 🔍 Pré-visualização dos dados")
            st.dataframe(df)

            # Gráfico 1: Total por Produto (barras horizontais)
            st.markdown("### 📦 Total vendido por Produto")
            produto_total = df.groupby("Produto")["Total"].sum().reset_index()
            fig1 = px.bar(produto_total, x="Total", y="Produto", orientation="h", text="Total")
            st.plotly_chart(fig1, use_container_width=True)

            # Gráfico 2: Evolução por Data
            st.markdown("### 📈 Evolução das vendas ao longo do tempo")
            evolucao = df.groupby("Data")["Total"].sum().reset_index()
            fig2 = px.line(evolucao, x="Data", y="Total", markers=True)
            st.plotly_chart(fig2, use_container_width=True)

            # Gráfico 3: Distribuição percentual por Categoria
            st.markdown("### 🧁 Participação por Categoria")
            categoria_total = df.groupby("Categoria")["Total"].sum().reset_index()
            fig3 = px.pie(categoria_total, names="Categoria", values="Total")
            st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.info("Envie um arquivo CSV para começar.")
