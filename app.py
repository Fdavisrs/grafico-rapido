import streamlit as st
import pandas as pd
import openai
import os
import unicodedata
from dotenv import load_dotenv

# Carrega variáveis do .env se existir
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuração da página
st.set_page_config(page_title="Gráfico Rápido + IA", layout="wide")
st.title("Gráfico Rápido \U0001F4C8 + IA")
st.markdown("Envie sua planilha CSV para visualização inteligente de métricas.")

# Upload do arquivo
file = st.file_uploader("Arraste ou selecione o arquivo CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file, sep=None, engine='python')

    # Padroniza os nomes das colunas
    def padronizar_nome(col):
        col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')
        return col.strip().lower().replace(" ", "_")

    df.columns = [padronizar_nome(col) for col in df.columns]

    st.subheader("\U0001F4C4 Pré-visualização dos dados")
    st.dataframe(df.head(), use_container_width=True)

    # Envia os nomes das colunas para a IA
    with st.spinner("Analisando colunas com IA..."):
        try:
            prompt = (
                "Abaixo está uma lista de colunas de uma planilha de vendas. "
                "Retorne apenas os nomes de colunas que indicam métricas quantitativas relevantes para análise (como total, valor, quantidade, vendas, etc.). "
                "Responda com uma lista Python simples.\n\nColunas:\n" + str(list(df.columns))
            )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            colunas_validas = eval(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Erro ao consultar a API da OpenAI: {e}")
            colunas_validas = []

    if colunas_validas:
        st.success(f"Colunas identificadas: {', '.join(colunas_validas)}")

        # Seleção de colunas para gerar gráfico
        col_x = st.selectbox("Escolha a coluna para o eixo X", df.columns)
        col_y = st.selectbox("Escolha a coluna para o eixo Y (somente numérica)", colunas_validas)

        if col_x and col_y:
            st.line_chart(df[[col_x, col_y]].dropna().set_index(col_x))
    else:
        st.error("A IA não conseguiu identificar colunas numéricas relevantes.")
