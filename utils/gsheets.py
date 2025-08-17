# utils/gsheets.py
import os
import json
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def conectar_planilha():
    """
    Conecta ao Google Sheets usando secret do Streamlit Cloud.
    Retorna a primeira aba da planilha.
    """
    # Lê credenciais do secret
    creds_info = json.loads(os.environ["GOOGLE_CREDS"])
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPE)

    # Autoriza e abre a planilha
    client = gspread.authorize(creds)
    sheet = client.open("streamlit_db").sheet1
    return sheet
