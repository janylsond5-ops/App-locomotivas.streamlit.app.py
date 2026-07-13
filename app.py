import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Consulta de Locomotivas", layout="centered")

DATA_FILE = "dados_locomotivas.csv"

# --- LISTA DE TERMOS MONITORADOS ---
TERMOS_DE_INTERESSE = [
    "jumper", "buzina", "vandalismo", "corrimão", "porta", 
    "manômetro", "tanque", "combustível", "corte", "furto", 
    "parabrisa", "traseira", "dianteira", "danificado", "quebrado", 
    "tampa", "janela", "farol", "bocal", "mangueira", "fuelink", "freio manual"
]

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
    df.columns = df.columns.str.strip() # Remove espaços extras nos nomes das colunas
    
    col1, col2 = st.columns(2)
    busca_ativo = col1.text_input("Buscar por Ativo:")
    busca_nota = col2.text_input("Buscar por Nº Nota:")

    if busca_ativo or busca_nota:
        if busca_ativo:
            resultado = df[df['Ativo'].astype(str).str.contains(busca_ativo, case=False, na=False)]
        else:
            resultado = df[df['Número Nota'].astype(str).str.contains(busca_nota, case=False, na=False)]
        
        if not resultado.empty:
            st.metric(label="Total de Notas Encontradas", value=len(resultado))
            
            # --- RAIO-X POR TAGS ---
            if 'Sumário' in resultado.columns:
                st.subheader("📊 Frequência de Ocorrências Críticas")
                sumarios_texto = " ".join(resultado['Sumário'].fillna('').astype(str).tolist()).lower()
                
                contagem = {}
                for termo in TERMOS_DE_INTERESSE:
                    if termo in sumarios_texto:
                        contagem[termo] = sumarios_texto.count(termo)
                
                if contagem:
                    st.bar_chart(pd.DataFrame.from_dict(contagem, orient='index', columns=['Qtd']))
            
            # --- EXIBIÇÃO DOS DETALHES ---
            for index, row in resultado.iterrows():
                with st.container(border=True):
                    st.subheader(f"Locomotiva: {str(row.get('Ativo', 'N/A'))}")
                    st.markdown(f"**Status:** {row.get('Status', 'N/A')}")
                    st.markdown(f"**Sumário:** {row.get('Sumário', 'Sem descrição')}")
                    st.markdown(f"**Data da Ocorrência:** {row.get('Data', 'N/A')}")
                    st.markdown(f"**Data de Abertura SAP:** {row.get('Criação', 'N/A')}")
                    st.info(f"Ocorrência: {row.get('Ocorrência', 'N/A')} | Nota: {row.get('Número Nota', 'N/A')}")
        else:
            st.warning("Nenhum dado encontrado.")
else:
    st.info("Aguardando carregamento da planilha pelo plantão.")
