import streamlit as st
import pandas as pd
import os
import io

st.title("Cadastro de Contatos - Semana Empresarial")

csv_file = "contatos.csv"

# Carrega os contatos existentes
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["contato", "nome"])

# Botão para importar CSV
st.subheader("Importar contatos via CSV")
file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])
if file is not None:
    try:
        try:
            imported_df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            imported_df = pd.read_csv(file, encoding='latin1')
        if not set(["contato", "nome"]).issubset(imported_df.columns):
            st.error("O arquivo CSV deve conter as colunas 'contato' e 'nome'.")
        else:
            contatos_invalidos = []
            contatos_validos = []
            for idx, row in imported_df.iterrows():
                contato = str(row['contato']).strip()
                nome = str(row['nome']).strip()
                if contato.startswith("+55") and len(contato) >= 13 and nome:
                    contatos_validos.append({"contato": contato, "nome": nome})
                else:
                    contatos_invalidos.append(f"Linha {idx+2}: {contato} - {nome}")
            if contatos_validos:
                df = pd.concat([df, pd.DataFrame(contatos_validos)], ignore_index=True)
                df.to_csv(csv_file, index=False)
                st.success(f"{len(contatos_validos)} contatos importados com sucesso!")
            if contatos_invalidos:
                st.warning("Contatos inválidos encontrados:\n" + "\n".join(contatos_invalidos))
    except Exception as e:
        st.error(f"Erro ao importar o arquivo: {e}")

# Formulário para adicionar novo contato
st.subheader("Adicionar contato manualmente")
with st.form("adicionar_contato"):
    contato = st.text_input("Número (formato: +55DDDNUMERO)", max_chars=15)
    nome = st.text_input("Nome")
    submitted = st.form_submit_button("Adicionar")

    if submitted:
        if contato.startswith("+55") and len(contato) >= 13 and nome.strip():
            novo = pd.DataFrame([[contato, nome]], columns=["contato", "nome"])
            df = pd.concat([df, novo], ignore_index=True)
            df.to_csv(csv_file, index=False)
            st.success(f"Contato {nome} adicionado com sucesso!")
        else:
            st.error("Preencha corretamente o número (+55DDDNUMERO) e o nome.")

# Exibe a lista de contatos
st.subheader("Contatos cadastrados")
st.dataframe(df)
