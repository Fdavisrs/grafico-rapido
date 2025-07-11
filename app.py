import streamlit as st
import pandas as pd
import altair as alt

st.title("Gráfico Rápido")
st.write("Envie sua planilha CSV")

uploaded_file = st.file_uploader("Upload", type="csv")

if uploaded_file is not None:
    try:
        # Lê a planilha usando ponto e vírgula
        df = pd.read_csv(uploaded_file, sep=';')

        st.subheader("Pré-visualização dos dados")
        st.dataframe(df)

        # Mostra apenas colunas válidas para X (todas) e para Y (numéricas)
        colunas_numericas = df.select_dtypes(include='number').columns.tolist()

        col_x = st.selectbox("Escolha a coluna para o eixo X", df.columns)
        col_y = st.selectbox("Escolha a coluna para o eixo Y (somente numérica)", colunas_numericas)

        if col_x != col_y:
            dados = df.groupby(col_x)[col_y].sum().reset_index()

            chart = alt.Chart(dados).mark_bar().encode(
                x=alt.X(col_x, sort="-y"),
                y=col_y,
                tooltip=[col_x, col_y]
            ).interactive()

            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("❗ Selecione colunas diferentes para X e Y.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao ler o arquivo: {e}")
