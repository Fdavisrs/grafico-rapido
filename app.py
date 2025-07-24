import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Título do app
st.set_page_config(layout="wide")
st.title("Análise de Vendas com Insights Automáticos")

# Botão para baixar modelo de planilha
modelo = pd.DataFrame(columns=["Data da Venda", "Produto", "Quantidade", "Valor Unitário", "Filial", "Total"])
modelo_csv = modelo.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📂 Baixar modelo de planilha",
    data=modelo_csv,
    file_name="modelo_planilha.csv",
    mime="text/csv"
)

# Upload do arquivo
arquivo = st.file_uploader("Faça upload da sua planilha de vendas (CSV ou Excel):", type=["csv", "xlsx"])

if arquivo is not None:
    try:
        if arquivo.name.endswith(".csv"):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)

        st.success("Arquivo carregado com sucesso!")

        # Normaliza nomes de colunas
        df.columns = df.columns.str.strip().str.lower()
        colunas_esperadas = ['data da venda', 'produto', 'quantidade', 'valor unitário', 'filial', 'total']
        if not all(col in df.columns for col in colunas_esperadas):
            st.error("A planilha deve conter as colunas: " + ", ".join(colunas_esperadas))
        else:
            # Visualiza dados
            st.subheader("Visualização dos dados")
            st.dataframe(df)

            # Gráfico
            st.subheader("Gráficos")
            col1, col2, col3 = st.columns(3)
            with col1:
                eixo_x = st.selectbox("Selecione o eixo X:", df.columns)
            with col2:
                eixo_y = st.selectbox("Selecione o eixo Y:", df.select_dtypes(include='number').columns)
            with col3:
                tipo_grafico = st.selectbox("Tipo de gráfico:", ["Barra", "Pizza", "Linha"])

            if eixo_x and eixo_y:
                agrupado = df.groupby(eixo_x)[eixo_y].sum().sort_values(ascending=False)
                fig, ax = plt.subplots()
                if tipo_grafico == "Barra":
                    agrupado.plot(kind='bar', ax=ax)
                elif tipo_grafico == "Linha":
                    agrupado.plot(kind='line', ax=ax)
                elif tipo_grafico == "Pizza":
                    agrupado.plot(kind='pie', ax=ax, autopct='%1.1f%%')
                    ax.set_ylabel('')
                st.pyplot(fig)

            # Insights automáticos
            st.subheader("🧰 Insights automáticos")
            try:
                total_vendas = df['total'].sum()
                produto_mais_vendido = df.groupby('produto')['quantidade'].sum().idxmax()
                produto_mais_valioso = df.groupby('produto')['total'].sum().idxmax()
                melhor_dia = df.groupby('data da venda')['total'].sum().idxmax()
                filial_top = df.groupby('filial')['total'].sum().idxmax()

                st.markdown(f"- **Total vendido:** R$ {total_vendas:,.2f}")
                st.markdown(f"- **Produto mais vendido (em quantidade):** {produto_mais_vendido}")
                st.markdown(f"- **Produto com maior valor de venda:** {produto_mais_valioso}")
                st.markdown(f"- **Dia com maior venda:** {melhor_dia}")
                st.markdown(f"- **Filial com maior venda:** {filial_top}")
            except Exception as e:
                st.warning(f"Não foi possível gerar todos os insights: {e}")

    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")

else:
    st.info("Por favor, envie um arquivo para começar.")
