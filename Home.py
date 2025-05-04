from pathlib import Path
from dotenv import load_dotenv
import os
import streamlit as st
import json
from RiotApi import GetPuuid, GetSummoner

load_dotenv()
api_key = os.getenv('RIOT_API_KEY')
st.session_state["api_key"] = api_key

st.set_page_config(page_title="Perfil League of Legends", layout="centered")
st.title("Sentinela")
col1, col2, col3 = st.columns([4, 1, 2])

with col1:
    nome = st.text_input("Nome do jogador", key="nome_input")

with col2:
    st.markdown("### #")

with col3:
    tag = st.text_input("Tag", key="tag_input")

dashboard_path = Path("pages/Dashboard.py")

if st.button("Buscar Perfil"):
    if nome and tag:
        with st.spinner("Buscando informações..."):
            puuid = GetPuuid(nome, tag, api_key)
            if puuid:
                dados = GetSummoner(puuid, api_key)
                if dados:

                    st.session_state['nome'] = nome
                    st.session_state['tag'] = tag
                    st.session_state['puuid'] = puuid
                    st.session_state['dados'] = dados
                    st.success("Perfil encontrado!")

                    st.switch_page(dashboard_path)
                else:
                    st.error("Não foi possível buscar os dados do invocador.")

    else:
        st.warning("Preencha todos os campos.")
