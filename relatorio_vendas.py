import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from utils.gsheets import conectar_planilha



def app():

    planilha = conectar_planilha()

    st.title("📈 Relatório de Vendas")

    planilha = conectar_planilha()
    dados = planilha.get_all_values()
    if len(dados) < 2:
        st.info("Nenhuma venda registrada ainda.")
        return

    df = pd.DataFrame(dados[1:], columns=dados[0])
    

    # Converte coluna 'date' para datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Converte colunas financeiras para numéricas (float)
    for col in ['sellPrice', 'price', 'valorParcela']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Filtros de data
    st.subheader("Filtrar por data")

    data_min = df['date'].min()
    data_max = df['date'].max()

    start_date = st.date_input("Data Inicial", value=data_min)
    end_date = st.date_input("Data Final", value=data_max)

    if start_date > end_date:
        st.error("Data inicial deve ser menor ou igual à data final.")
        return

    # Filtra o DataFrame
    df_filtrado = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

    st.subheader(f"Resultados entre {start_date} e {end_date}")

    if df_filtrado.empty:
        st.warning("Nenhum registro encontrado para o período selecionado.")
        return

    # Mostra o dataframe filtrado
    st.dataframe(df_filtrado)

    # Soma os valores desejados
    soma_sellPrice = df_filtrado['sellPrice'].sum()
    soma_price = df_filtrado['price'].sum()
    soma_valorParcela = df_filtrado['valorParcela'].sum()

    # Exibe os totais
    st.markdown("---")
    st.write(f"**Total Valor da Venda (sellPrice) :** R$ {soma_sellPrice:,.2f}")
    st.write(f"**Total Preço do Produto (price) :** R$ {soma_price:,.2f}")
    st.write(f"**Total Valor das Parcelas (valorParcela) :** R$ {soma_valorParcela:,.2f}")
