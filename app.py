import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Consulta de Locomotivas", layout="centered")

st.title("🔍 Consulta de Locomotivas")

# --- LÓGICA DE ADMIN ---
# Substitua 'senha123' por uma senha segura
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if not st.session_state.password_correct:
        with st.expander("🔐 Acesso Plantão (Admin)"):
            pwd = st.text_input("Senha", type="password")
            if st.button("Logar"):
                if pwd == "senha123": # Troque a senha aqui
                    st.session_state.password_correct = True
                    st.rerun()
    else:
        if st.button("Sair do modo Admin"):
            st.session_state.password_correct = False
            st.rerun()

check_password()

# --- UPLOAD DE DADOS ---
if st.session_state.get("password_correct"):
    uploaded_file = st.file_uploader("Substituir planilha (Acesso restrito)", type=['xls', 'xlsx'])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df.to_csv("dados_locomotivas.csv", index=False) # Salva internamente
        st.success("Planilha atualizada com sucesso!")

# --- BUSCA PARA O CAMPO ---
try:
    df = pd.read_csv("dados_locomotivas.csv")
    
    col1, col2 = st.columns(2)
    busca_ativo = col1.text_input("Buscar por Ativo (Locomotiva):")
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
            
except FileNotFoundError:
    st.error("Nenhuma planilha carregada. Peça ao plantão para realizar o upload.")
