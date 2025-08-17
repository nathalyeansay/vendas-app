import streamlit as st
import vendas_app_clean.cadastro_vendas as cadastro
import vendas_app_clean.busca_vendas as busca
import vendas_app_clean.relatorio_vendas as relatorio


PAGES = {
    "Cadastro de Vendas": "cadastro_vendas",
    "Buscar Vendas": "busca_vendas",
    "Relatório de Vendas": "relatorio_vendas"
}

#PAGE lAYOUT
st.set_page_config(
    page_title="teste",
    layout='wide',
)
##

st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para:", list(PAGES.keys()))

if page == "Cadastro de Vendas":
    import vendas_app_clean.cadastro_vendas as cadastro
    cadastro.app()  # sua função principal em cadastro_vendas.py
elif page == "Buscar Vendas":
    import vendas_app_clean.busca_vendas as busca
    busca.app()   
elif page == "Relatório de Vendas":
    import vendas_app_clean.relatorio_vendas as relatorio
    relatorio.app()   # sua função principal em busca_vendas.py
