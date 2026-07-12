import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consulta Locomotivas", layout="centered")

st.title("🔍 Consulta de Locomotivas")

# Tenta carregar o arquivo fixo que você subiu no GitHub
try:
    df = pd.read_excel("dados.xlsx")
except:
    st.error("Arquivo de dados não encontrado. Entre em contato com o suporte.")
    st.stop()

# Campo de busca para o campo
col1, col2 = st.columns(2)
busca_ativo = col1.text_input("Buscar por Ativo:")
busca_nota = col2.text_input("Buscar por Nº Nota:")

if busca_ativo or busca_nota:
    if busca_ativo:
        resultado = df[df['Ativo'].astype(str).str.contains(busca_ativo, case=False)]
    else:
        resultado = df[df['Número Nota'].astype(str).str.contains(busca_nota, case=False)]
    
    if not resultado.empty:
        for index, row in resultado.iterrows():
            with st.container(border=True):
                st.subheader(f"Locomotiva: {row['Ativo']}")
                st.markdown(f"**Status:** {row['Status']}")
                st.markdown(f"**Sumário:** {row['Sumário']}")
                st.info(f"Ocorrência: {row['Ocorrência']} | Nota: {row['Número Nota']}")
    else:
        st.warning("Nenhum dado encontrado.")
