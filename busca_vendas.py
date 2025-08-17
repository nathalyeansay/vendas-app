import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from utils.gsheets import conectar_planilha



def app():

    planilha = conectar_planilha()

    st.title("📊 Relatório de Vendas")

    # Conecta e lê os dados
    planilha = conectar_planilha()
    dados = planilha.get_all_values()  # pega todas as linhas

    # Converte para DataFrame
    df = pd.DataFrame(dados[1:], columns=dados[0])  # pula cabeçalho na 1ª linha

    df['id_auto'] = df['id_auto'].astype(int)

    # Renomeia colunas para apelidos mais amigáveis
    df = df.rename(columns={
        "id_auto": "ID da Venda",
        "date": "Data",
        "code": "Código Produto",
        "price": "Preço",
        "name": "Nome Produto",
        "info": "Info",
        "client": "Cliente",
        "sellPrice": "Valor de Venda",
        "qtdd": "Qtdd Parcelas",
        "valorParcela": "Valor da Parcela"
        # inclua outras colunas conforme os nomes reais do seu header
    })

    # Exibe no Streamlit
    st.dataframe(df)

    # Se houver dados, permite excluir
    if not df.empty:
        st.subheader("🗑️ Excluir Venda")

        # Seleciona um ID para excluir
        id_para_excluir = st.selectbox('Selecione o ID para excluir:', df['ID da Venda'].tolist())

        if st.button('Excluir'):
            try:
                # Encontra o índice da linha com o ID
                index = int(df[df['ID da Venda'] == int(id_para_excluir)].index[0])

                # Remove a linha na planilha (considerando header na linha 1, somamos +2)
                planilha.delete_rows(index + 2)

                st.success(f"✅ Venda com ID {id_para_excluir} excluída com sucesso!")
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()
                    
    # Atualiza a página

            except Exception as e:
                st.error(f"❌ Erro ao excluir: {e}")
    else:
        st.info("Nenhuma venda registrada ainda.")