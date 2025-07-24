import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

st.set_page_config(page_title="Analisador de Vendas", layout="wide")
st.title("📊 Analisador de Vendas")

# Função para gerar CSV modelo
def gerar_csv_modelo():
    df_modelo = pd.DataFrame({
        "data": ["2025-01-01", "2025-01-02"],
        "produto": ["Pão Francês", "Croissant"],
        "quantidade": [120, 35],
        "valor_unitario": [0.50, 3.00],
        "total": [60.00, 105.00]
    })
    return df_modelo.to_csv(index=False).encode("utf-8")

# Botão para download do modelo
csv_modelo = gerar_csv_modelo()
b64 = base64.b64encode(csv_modelo).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="modelo_vendas.csv">📥 Baixar modelo de planilha</a>'
st.markdown(href, unsafe_allow_html=True)

st.markdown("Faça upload de uma planilha no formato **modelo_vendas.csv** para visualizar os dados.")

uploaded_file = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, parse_dates=["data"])
        df.columns = df.columns.str.strip().str.lower()

        # Verificação de colunas obrigatórias
        colunas_obrigatorias = {"data", "produto", "quantidade", "valor_unitario", "total"}
        if not colunas_obrigatorias.issubset(set(df.columns)):
            st.error("❌ A planilha está fora do padrão. Verifique se ela contém as colunas: data, produto, quantidade, valor_unitario e total.")
        else:
            # Filtros
            st.sidebar.header("Filtros")
            produtos = st.sidebar.multiselect("Produto", df["produto"].unique(), default=df["produto"].unique())
            datas = st.sidebar.date_input("Período", [df["data"].min(), df["data"].max()])

            # Aplicando filtros
            df_filtrado = df[
                (df["produto"].isin(produtos)) &
                (df["data"] >= pd.to_datetime(datas[0])) &
                (df["data"] <= pd.to_datetime(datas[1]))
            ]

            st.subheader("Tabela de Vendas Filtrada")
            st.dataframe(df_filtrado)

            # Gráficos
            st.subheader("Total de Vendas por Produto")
            vendas_produto = df_filtrado.groupby("produto")["total"].sum().sort_values(ascending=False)
            fig1, ax1 = plt.subplots()
            vendas_produto.plot(kind="bar", ax=ax1)
            ax1.set_ylabel("Total R$")
            st.pyplot(fig1)

            st.subheader("Evolução Diária das Vendas")
            vendas_diarias = df_filtrado.groupby("data")["total"].sum()
            fig2, ax2 = plt.subplots()
            vendas_diarias.plot(kind="line", marker='o', ax=ax2)
            ax2.set_ylabel("Total R$")
            st.pyplot(fig2)

            st.subheader("Participação por Produto")
            fig3, ax3 = plt.subplots()
            vendas_produto.plot(kind="pie", autopct="%1.1f%%", ax=ax3)
            ax3.set_ylabel("")
            st.pyplot(fig3)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.warning("⚠️ Nenhum arquivo enviado ainda. Faça upload de um CSV com as colunas: data, produto, quantidade, valor_unitario, total.")
