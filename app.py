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
    
    col1, col2 = st.columns(2)
    busca_ativo = col1.text_input("Buscar por Ativo:")
    busca_nota = col2.text_input("Buscar por Nº Nota:")

    if busca_ativo or busca_nota:
        if busca_ativo:
            resultado = df[df['Ativo'].astype(str).str.contains(busca_ativo, case=False)]
        else:
            resultado = df[df['Número Nota'].astype(str).str.contains(busca_nota, case=False)]
        
        if not resultado.empty:
            st.metric(label="Total de Notas Encontradas", value=len(resultado))
            
            # --- RAIO-X POR TAGS ---
# --- RAIO-X POR TAGS (Versão Corrigida) ---
            st.subheader("📊 Frequência de Ocorrências Críticas")
            
            # Forçamos o uso do nome exato que você confirmou que existe
            col_nome = "Sumário"
            
            if col_nome in resultado.columns:
                # O preenchimento .fillna('') resolve o erro de valor vazio
                sumarios_texto = " ".join(resultado[col_nome].fillna('').astype(str).tolist()).lower()
                
                contagem = {}
                for termo in TERMOS_DE_INTERESSE:
                    if termo in sumarios_texto:
                        contagem[termo] = sumarios_texto.count(termo)
                
                if contagem:
                    st.bar_chart(pd.DataFrame.from_dict(contagem, orient='index', columns=['Qtd']))
                else:
                    st.write("Nenhum termo crítico identificado.")
            else:
                st.error(f"Coluna '{col_nome}' não encontrada na planilha.")
            
            # Exibição dos Detalhes
            for index, row in resultado.iterrows():
                with st.container(border=True):
                    st.subheader(f"Locomotiva: {row['Ativo']}")
                    st.markdown(f"**Status:** {row['Status']}")
                    # Exibição segura do Sumário
                    val_sumario = row[col_nome] if col_nome in row else "Sem descrição"
                    st.markdown(f"**Sumário:** {val_sumario}")
                    st.markdown(f"**Data da Ocorrência:** {row['Data']}")
                    st.markdown(f"**Data de Abertura SAP:** {row['Criação']}")
                    st.info(f"Ocorrência: {row['Ocorrência']} | Nota: {row['Número Nota']}")
            
            # Exibição dos Detalhes
            for index, row in resultado.iterrows():
                with st.container(border=True):
                    st.subheader(f"Locomotiva: {row['Ativo']}")
                    st.markdown(f"**Status:** {row['Status']}")
                    # Usa a coluna correta encontrada para exibir o sumário
                    st.markdown(f"**Sumário:** {row[col_sumario] if col_sumario else 'Não disponível'}")
                    st.markdown(f"**Data da Ocorrência:** {row['Data']}")
                    st.markdown(f"**Data de Abertura SAP:** {row['Criação']}")
                    st.info(f"Ocorrência: {row['Ocorrência']} | Nota: {row['Número Nota']}")
        else:
            st.warning("Nenhum dado encontrado.")
else:
    st.info("Aguardando carregamento da planilha pelo plantão.")
