# utils/gsheets.py
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

# Conectando Planilha Google com Streamlit Secrets
@st.cache_resource
def conectar_planilha():
    try:
        # Lê as credenciais diretamente do Streamlit Secrets
        creds_info = st.secrets["google"]  # agora já é um dicionário

        # Cria as credenciais de serviço
        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=[
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
        )

        # Autoriza o cliente gspread
        client = gspread.authorize(creds)

        # Abre a planilha
        sheet_name = "streamlit_db"  # Nome da sua planilha
        sheet = client.open(sheet_name).sheet1
        return sheet

    except Exception as e:
        st.error(f"Erro ao conectar com a planilha: {e}")
        return None
