import streamlit as st
import pandas as pd
import os
from collections import Counter

st.set_page_config(page_title="Consulta de Locomotivas", layout="centered")

DATA_FILE = "dados_locomotivas.csv"

st.title("🔍 Consulta de Locomotivas")

# --- ÁREA ADMINISTRATIVA ---
with st.expander("🔐 Acesso Plantão"):
    senha = st.text_input("Senha de Acesso", type="password")
    if senha == "12345":
        uploaded_file = st.file_uploader("Substituir planilha atual", type=['xls', 'xlsx'])
        if uploaded_file:
            df_novo = pd.read_excel(uploaded_file)
            df_novo.to_csv(DATA_FILE, index=False)
            st.success("Dados atualizados!")
    else:
        st.write("Acesso restrito.")

# --- BUSCA PARA O CAMPO ---
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    
    col1, col2 = st.columns(2)
    busca_ativo = col1.text_input("Buscar por Ativo:")
    busca_nota = col2.text_input("Buscar por Nº Nota:")

    if busca_ativo or busca_nota:
        if busca_ativo:
            resultado = df[df['Ativo'].astype(str).str.contains(busca_ativo, case=False)]
        else:
            resultado = df[df['Número Nota'].astype(str).str.contains(busca_nota, case=False)]
        
        if not resultado.empty:
            # Card de Resumo
            st.metric(label="Total de Notas Encontradas", value=len(resultado))
            
            # --- ANÁLISE DE FREQUÊNCIA (Raio-X) ---
            st.subheader("📊 Frequência de Problemas")
            # Pega o sumário, transforma em lista de palavras, ignora palavras curtas
            palavras = " ".join(resultado['Sumário'].astype(str).tolist()).split()
            palavras_filtradas = [p for p in palavras if len(p) > 4] # Ignora palavras muito curtas
            contagem = pd.DataFrame.from_dict(Counter(palavras_filtradas), orient='index', columns=['Qtd'])
            st.bar_chart(contagem.sort_values(by='Qtd', ascending=False).head(5))
            
            # Exibição dos Detalhes
            for index, row in resultado.iterrows():
                with st.container(border=True):
                    st.subheader(f"Locomotiva: {row['Ativo']}")
                    st.markdown(f"**Status:** {row['Status']}")
                    st.markdown(f"**Sumário:** {row['Sumário']}")
                    st.markdown(f"**Data da Ocorrência:** {row['Data']}")
                    st.markdown(f"**Data de Abertura SAP:** {row['Criação']}")
                    st.info(f"Ocorrência: {row['Ocorrência']} | Nota: {row['Número Nota']}")
        else:
            st.warning("Nenhum dado encontrado.")
else:
    st.info("Aguardando carregamento da planilha pelo plantão.")
