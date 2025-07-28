import streamlit as st
import pandas as pd
import os
import io
import pywhatkit
import time

st.title("Cadastro de Contatos - Semana Empresarial")

csv_file = "contatos.csv"

# Carrega os contatos existentes
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file, dtype={'contato': str})
    # Adiciona coluna de status se não existir
    if 'status' not in df.columns:
        df['status'] = 'Pendente'
    if 'selecionado' not in df.columns:
        df['selecionado'] = False
else:
    df = pd.DataFrame(columns=["contato", "nome", "status", "selecionado"])

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
                # Adiciona colunas de status e seleção para novos contatos
                for contato in contatos_validos:
                    contato['status'] = 'Pendente'
                    contato['selecionado'] = False
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
    contato = st.text_input("Número (formato: +55DDDNUMERO ou 55DDDNUMERO)", max_chars=15)
    nome = st.text_input("Nome")
    submitted = st.form_submit_button("Adicionar")

    if submitted:
        # Limpa e formata o número
        contato_limpo = str(contato).strip()
        if not contato_limpo.startswith("+") and contato_limpo.startswith("55"):
            contato_limpo = "+" + contato_limpo
        
        if contato_limpo.startswith("+55") and len(contato_limpo) >= 13 and nome.strip():
            novo = pd.DataFrame([[contato_limpo, nome, 'Pendente', False]], columns=["contato", "nome", "status", "selecionado"])
            df = pd.concat([df, novo], ignore_index=True)
            df.to_csv(csv_file, index=False)
            st.success(f"Contato {nome} adicionado com sucesso!")
        else:
            st.error("Preencha corretamente o número (+55DDDNUMERO ou 55DDDNUMERO) e o nome.")

# Seção para gerenciar contatos existentes
st.subheader("Gerenciar contatos")
if len(df) > 0:
    # Selecionar contato para editar/deletar
    contatos_lista = [f"{row['nome']} ({row['contato']})" for index, row in df.iterrows()]
    contato_selecionado = st.selectbox("Selecione um contato para gerenciar:", contatos_lista)
    
    if contato_selecionado:
        # Encontrar o índice do contato selecionado
        index_selecionado = contatos_lista.index(contato_selecionado)
        contato_atual = df.iloc[index_selecionado]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✏️ Editar contato"):
                st.session_state.editando = True
                st.session_state.index_editando = index_selecionado
        
        with col2:
            if st.button("🗑️ Deletar contato", type="secondary"):
                if st.button("⚠️ Confirmar exclusão", type="primary"):
                    df = df.drop(index_selecionado).reset_index(drop=True)
                    df.to_csv(csv_file, index=False)
                    st.success(f"Contato {contato_atual['nome']} deletado com sucesso!")
                    st.rerun()
        
        # Formulário de edição
        if st.session_state.get('editando', False) and st.session_state.get('index_editando') == index_selecionado:
            with st.form("editar_contato"):
                novo_contato = st.text_input("Novo número:", value=contato_atual['contato'], max_chars=15)
                novo_nome = st.text_input("Novo nome:", value=contato_atual['nome'])
                
                col3, col4 = st.columns(2)
                with col3:
                    if st.form_submit_button("💾 Salvar alterações"):
                        # Limpa e formata o número
                        contato_limpo = str(novo_contato).strip()
                        if not contato_limpo.startswith("+") and contato_limpo.startswith("55"):
                            contato_limpo = "+" + contato_limpo
                        
                        if contato_limpo.startswith("+55") and len(contato_limpo) >= 13 and novo_nome.strip():
                            df.at[index_selecionado, 'contato'] = contato_limpo
                            df.at[index_selecionado, 'nome'] = novo_nome
                            df.to_csv(csv_file, index=False)
                            st.success("Contato atualizado com sucesso!")
                            st.session_state.editando = False
                            st.rerun()
                        else:
                            st.error("Preencha corretamente o número (+55DDDNUMERO ou 55DDDNUMERO) e o nome.")
                
                with col4:
                    if st.form_submit_button("❌ Cancelar"):
                        st.session_state.editando = False
                        st.rerun()
else:
    st.info("Nenhum contato cadastrado ainda.")

# Seção para selecionar contatos para envio
st.subheader("Selecionar contatos para envio")
if len(df) > 0:
    # Botões para selecionar/desselecionar todos
    col_sel1, col_sel2, col_sel3 = st.columns(3)
    with col_sel1:
        if st.button("✅ Selecionar todos"):
            df['selecionado'] = True
            df.to_csv(csv_file, index=False)
            st.rerun()
    with col_sel2:
        if st.button("❌ Desselecionar todos"):
            df['selecionado'] = False
            df.to_csv(csv_file, index=False)
            st.rerun()
    with col_sel3:
        if st.button("🔄 Resetar status"):
            df['status'] = 'Pendente'
            df.to_csv(csv_file, index=False)
            st.rerun()
    
    # Lista de contatos com checkboxes
    st.write("**Selecione os contatos que devem receber a mensagem:**")
    for index, row in df.iterrows():
        col_check, col_info = st.columns([1, 4])
        with col_check:
            selecionado = st.checkbox("", value=row['selecionado'], key=f"check_{index}")
            if selecionado != row['selecionado']:
                df.at[index, 'selecionado'] = selecionado
                df.to_csv(csv_file, index=False)
        with col_info:
            status_emoji = "✅" if row['status'] == 'Enviado' else "⏳" if row['status'] == 'Pendente' else "❌"
            st.write(f"{status_emoji} **{row['nome']}** ({row['contato']}) - {row['status']}")

# Seção para escrever a mensagem
st.subheader("Configurar mensagem")
mensagem_padrao = """Olá, {contato}! 👋

Você participou da edição passada da Semana Empresarial de Açailândia e tornou esse evento ainda mais especial. Por isso, temos o prazer de convidar você novamente para a **Semana Empresarial 2025**! 🚀

📅 As palestras acontecerão nos dias:
- Terça-feira, 29 de julho
- Quarta-feira, 30 de julho

Serão dois dias de muito aprendizado, networking e inspiração com grandes nomes do empreendedorismo e inovação.

🎯 Garanta já a sua vaga e faça sua inscrição pelo link:
https://www.semanaempresarial.com.br/markplace-eventos/

Contamos com a sua presença para fazer desta edição a melhor de todas. Vamos juntos transformar ideias em resultados! 💼✨

🎁 **Use o cupom especial:** `talk#magna` para garantir seu desconto exclusivo! 🏷️

Te vejo lá!"""

mensagem = st.text_area("Mensagem a ser enviada", value=mensagem_padrao, height=300, help="Use {contato} para personalizar com o nome do participante")

# Botão para executar o envio
st.subheader("Enviar mensagens")

# Controle de estado para parar o envio
if 'enviando' not in st.session_state:
    st.session_state.enviando = False
if 'envio_concluido' not in st.session_state:
    st.session_state.envio_concluido = False
if 'contatos_processados' not in st.session_state:
    st.session_state.contatos_processados = []

col_envio1, col_envio2 = st.columns(2)

with col_envio1:
    if st.button("🚀 Executar envio das mensagens", type="primary", disabled=st.session_state.enviando):
        st.session_state.enviando = True
        st.session_state.envio_concluido = False
        st.session_state.contatos_processados = []
        st.rerun()

with col_envio2:
    if st.button("⏹️ Parar envio", type="secondary", disabled=not st.session_state.enviando):
        st.session_state.enviando = False
        st.session_state.contatos_processados = []
        st.rerun()

# Executa o envio apenas uma vez quando iniciado
if st.session_state.enviando and not st.session_state.envio_concluido:
    # Filtra apenas contatos selecionados
    df_selecionados = df[df['selecionado'] == True]
    
    if len(df_selecionados) == 0:
        st.error("Nenhum contato selecionado para envio. Selecione pelo menos um contato.")
        st.session_state.enviando = False
    else:
        st.info("⚠️ Certifique-se de que o WhatsApp Web está aberto e logado no navegador!")
        st.info(f"📤 Enviando para {len(df_selecionados)} contato(s) selecionado(s)...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        contatos_enviados = 0
        contatos_erro = 0
        
        for index, row in df_selecionados.iterrows():
            # Verifica se o usuário quer parar
            if not st.session_state.enviando:
                break
                
            numero = str(row['contato']).strip()
            nome = row['nome'] if 'nome' in df.columns and pd.notna(row['nome']) else numero
            
            # Verifica se já foi processado
            if numero in st.session_state.contatos_processados:
                continue
                
            if not numero.startswith("+55") or len(numero) < 13:
                contatos_erro += 1
                df.at[index, 'status'] = 'Erro'
                st.session_state.contatos_processados.append(numero)
                continue
                
            msg = mensagem.format(contato=nome)
            status_text.text(f"📤 Enviando para {nome} ({numero})... ({contatos_enviados + 1}/{len(df_selecionados)})")
            
            try:
                pywhatkit.sendwhatmsg_instantly(numero, msg, wait_time=15, tab_close=True)
                contatos_enviados += 1
                df.at[index, 'status'] = 'Enviado'
                st.success(f"✅ Enviado para {nome} ({numero})")
                st.session_state.contatos_processados.append(numero)
                time.sleep(15)  # Aguarda mais tempo entre mensagens
            except Exception as e:
                contatos_erro += 1
                df.at[index, 'status'] = 'Erro'
                st.error(f"❌ Erro ao enviar para {numero}: {e}")
                st.session_state.contatos_processados.append(numero)
            
            progress_bar.progress((contatos_enviados + contatos_erro) / len(df_selecionados))
        
        # Salva o status atualizado
        df.to_csv(csv_file, index=False)
        
        progress_bar.progress(100)
        status_text.text("✅ Envio concluído!")
        st.success(f"✅ Envio concluído! {contatos_enviados} mensagens enviadas, {contatos_erro} erros.")
        st.session_state.enviando = False
        st.session_state.envio_concluido = True

# Exibe a lista de contatos
st.subheader("Contatos cadastrados")
# Mostra apenas as colunas principais para melhor visualização
df_display = df[['nome', 'contato', 'status', 'selecionado']].copy()
st.dataframe(df_display, use_container_width=True)
