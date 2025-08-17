import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from utils.gsheets import conectar_planilha



def app():

    planilha = conectar_planilha()
    

    def clean_txt(texto):
        return texto.encode('utf-8', 'ignore').decode().strip()


    st.title("📋 Cadastro de Vendas")

    planilha = conectar_planilha()
    dados = planilha.get_all_values()
    df = pd.DataFrame(dados[1:], columns=dados[0])  # ignora cabeçalho

    # EDIÇÃO
    st.subheader("✏️ Editar Produto")
    id_edicao = st.text_input("Digite o ID do produto que deseja editar:")

    if st.button("Carregar"):
        if id_edicao and id_edicao.isdigit():
            id_edicao_int = int(id_edicao)
            linha = df[df['id_auto'] == str(id_edicao_int)]

            if not linha.empty:
                st.session_state.edit_data = {
                    "date": linha.iloc[0]["date"],
                    "code": linha.iloc[0]["code"],               # aqui use 'code'
                    "price": float(linha.iloc[0]["price"]),
                    "name": linha.iloc[0]["name"],
                    "info": linha.iloc[0]["info"],
                    "client": linha.iloc[0]["client"],
                    "sellPrice": float(linha.iloc[0]["sellPrice"]),
                    "qtdd": int(linha.iloc[0]["qtdd"])
            }
            else:
                st.error("❌ ID não encontrado.")

    # Preenche os campos com dados salvos (se houver)
    edit_data = st.session_state.get("edit_data", {})

    date = st.date_input('Data da Venda', value=pd.to_datetime(edit_data.get("date", None)) if edit_data.get("date") else None)
    code = st.text_input('Código do Produto:', value=edit_data.get("code", ""), placeholder='000 000 000')
    price = st.number_input('Preço do Produto', value=edit_data.get("price", None), placeholder='1000,00')
    name = st.text_input('Nome do Produto', value=edit_data.get("name", ""))
    info = st.text_area('Descrição do Produto', value=edit_data.get("info", ""))
    client = st.text_input('Cliente:', value=edit_data.get("client", ""), placeholder='nome')
    sellPrice = st.number_input('Valor da Venda', value=edit_data.get("sellPrice", None), placeholder='1000,00')
    qtdd = st.number_input('Número de Parcelas:', min_value=1, value=edit_data.get("qtdd", 1))

    valorParcela = round(sellPrice / qtdd, 2) if sellPrice and qtdd else 0.00
    st.text(f"Valor da Parcela: R$ {valorParcela:.2f}")

    # BOTÕES: Salvar novo OU Atualizar
    col1, col2 = st.columns(2)

    with col1:
        if st.button('Salvar'):
            try:
                id_auto = len(planilha.get_all_values())

                new_line = [
                    id_auto,
                    date.isoformat(),
                    code.strip(),
                    float(price),
                    name,
                    info,
                    client,
                    float(sellPrice),
                    int(qtdd),
                    float(valorParcela)
                ]

                planilha.append_row(new_line)
                st.success('✅ Venda Salva com Sucesso')
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")

    with col2:
        if st.button('Atualizar') and "edit_data" in st.session_state:
            try:
                index = df[df['id_auto'] == str(id_edicao)].index[0]
                linha_excel = index + 2  # soma cabeçalho
                nova_linha = [
                    id_edicao,
                    date.isoformat(),
                    code.strip(),
                    float(price),
                    name,
                    info,
                    client,
                    float(sellPrice),
                    int(qtdd),
                    float(valorParcela)
                ]
                planilha.update(f'A{linha_excel}:J{linha_excel}', [nova_linha])
                st.success(f'✅ Venda com ID {id_edicao} atualizada com sucesso!')
                st.rerun()

            except Exception as e:
                st.error(f"❌ Erro ao atualizar: {e}")