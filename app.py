import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Análise de Vendas com Insights Automáticos", layout="centered")

st.title("📊 Análise de Vendas com Insights Automáticos")

# Planilha modelo embutida como string
modelo_csv = """data da venda,produto,quantidade,valor unitário,filial,total
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
,,,,,
"""

# Botão de download da planilha modelo
st.download_button(
    label="📥 Baixar modelo de planilha",
    data=modelo_csv,
    file_name="modelo_planilha_vendas.csv",
    mime="text/csv",
)

# Upload de planilha
uploaded_file = st.file_uploader("Faça upload da sua planilha de vendas (CSV ou Excel):", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Verifica se colunas obrigatórias existem
        colunas_esperadas = ["data da venda", "produto", "quantidade", "valor unitário", "filial", "total"]
        if not all(col in df.columns for col in colunas_esperadas):
            st.error("❌ A planilha deve conter as colunas: data da venda, produto, quantidade, valor unitário, filial, total")
        else:
            st.success("✅ Arquivo carregado com sucesso!")
            st.write("Visualização dos dados:")
            st.dataframe(df)

            # Insights automáticos
            st.subheader("🔍 Insights automáticos")
            try:
                df["data da venda"] = pd.to_datetime(df["data da venda"], errors="coerce")
                df = df.dropna(subset=["data da venda"])

                melhor_dia = df.groupby("data da venda")["total"].sum().idxmax()
                maior_venda = df.loc[df["total"].idxmax()]
                produto_mais_vendido = df.groupby("produto")["quantidade"].sum().idxmax()
                filial_top = df.groupby("filial")["total"].sum().idxmax()

                st.markdown(f"📅 **Dia com maior faturamento:** {melhor_dia.date()}")
                st.markdown(f"💰 **Maior venda:** {maior_venda['produto']} – R$ {maior_venda['total']:.2f}")
                st.markdown(f"🔥 **Produto mais vendido (em quantidade):** {produto_mais_vendido}")
                st.markdown(f"🏪 **Filial com maior faturamento:** {filial_top}")

            except Exception as e:
                st.warning("Não foi possível gerar insights automáticos.")
                st.exception(e)

    except Exception as e:
        st.error("Erro ao processar o arquivo.")
        st.exception(e)
