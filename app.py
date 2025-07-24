import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gráfico Rápido com GPT", layout="wide")

st.title("📊 Gráfico Rápido com GPT")
st.caption("📂 Envie sua planilha (.csv ou .xlsx)")

# Upload
uploaded_file = st.file_uploader("Drag and drop file here", type=["csv", "xlsx"])

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    
    try:
        if file_ext == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == "xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Formato de arquivo não suportado.")
            st.stop()
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
        st.stop()

    st.success("✅ Arquivo carregado com sucesso!")
    st.dataframe(df.head(50), use_container_width=True)

    # Separar colunas categóricas e numéricas
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if not categorical_cols or not numeric_cols:
        st.warning("A planilha precisa ter pelo menos uma coluna categórica e uma numérica.")
        st.stop()

    x_axis = st.selectbox("Escolha o eixo X (categoria):", categorical_cols)
    y_axis = st.selectbox("Escolha o eixo Y (valor numérico):", numeric_cols)
    chart_type = st.selectbox("Tipo de gráfico:", ["Barra", "Linha", "Pizza"])

    df_grouped = df.groupby(x_axis)[y_axis].sum().reset_index()

    if chart_type == "Barra":
        fig = px.bar(df_grouped, x=x_axis, y=y_axis)
    elif chart_type == "Linha":
        fig = px.line(df_grouped, x=x_axis, y=y_axis)
    elif chart_type == "Pizza":
        fig = px.pie(df_grouped, names=x_axis, values=y_axis)

    st.plotly_chart(fig, use_container_width=True)
