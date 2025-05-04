import streamlit as st
from RiotApi import GetMatchIds, GetMatchData
import matplotlib.pyplot as plt
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Resumo do Jogador", layout="wide")

if "nome" not in st.session_state:
    st.warning("Jogador não encontrado")
    st.stop()

# Dados do jogador
nome = st.session_state["nome"]
puuid = st.session_state["puuid"]
api_key = st.session_state["api_key"]
dados = st.session_state["dados"]
nivel = dados["summonerLevel"]
icone = dados["profileIconId"]


def carregar_icone(icone_id):
    url = f"http://ddragon.leagueoflegends.com/cdn/13.6.1/img/profileicon/{icone_id}.png"
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


with st.sidebar:
    st.image(carregar_icone(icone), width=100)
    st.markdown(f"### {nome}")
    st.markdown(f"Nível {nivel}")
    st.markdown("---")
    st.write("------------.")

# Pega os dados das partidas
match_ids = GetMatchIds(puuid, api_key, count=5)

dados_partidas = []
for match_id in match_ids:
    dados = GetMatchData(match_id, api_key)
    if dados:
        for jogador in dados["info"]["participants"]:
            if jogador["puuid"] == puuid:
                dados_partidas.append({
                    "match_id": match_id,
                    "champion": jogador["championName"],
                    "kills": jogador["kills"],
                    "deaths": jogador["deaths"],
                    "assists": jogador["assists"],
                    "gold": jogador["goldEarned"],
                    "damage": jogador["totalDamageDealtToChampions"],
                    "win": jogador["win"]
                })

st.markdown("## Últimas Partidas")
cols = st.columns(5)
for i, partida in enumerate(dados_partidas):
    with cols[i]:
        st.metric(label=partida["champion"], value="✅" if partida["win"] else "❌")
        st.write(f'**KDA:** {partida["kills"]}/{partida["deaths"]}/{partida["assists"]}')
        st.write(f'**Dano:** {partida["damage"]}')
        st.write(f'**Gold:** {partida["gold"]}')

st.markdown("---")
st.markdown("## Gráficos de Desempenho")

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("🔸 Dano por Campeão")
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    campeoes = [p["champion"] for p in dados_partidas]
    danos = [p["damage"] for p in dados_partidas]
    ax.bar(campeoes, danos, color='deepskyblue')
    ax.set_ylabel("Dano causado")
    ax.set_xlabel("Campeão")
    st.pyplot(fig)

# gráfico 2: ouro
with col2:
    st.subheader("💰 Ouro ganho por partida")
    fig_gold, ax_gold = plt.subplots(figsize=(6, 4))
    campeoes = [p["champion"] for p in dados_partidas]
    ouro = [p["gold"] for p in dados_partidas]
    ax_gold.bar(campeoes, ouro, color='gold')
    ax_gold.set_ylabel("Ouro ganho")
    ax_gold.set_xlabel("Campeão")
    ax_gold.set_title("Ouro por partida")
    st.pyplot(fig_gold)

# grafico 3: KDA por Partida
with col3:
    st.subheader("⚔️ KDA por Partida")
    fig, ax = plt.subplots()
    kdas = [ (p["kills"] + p["assists"]) / (p["deaths"] if p["deaths"] != 0 else 1) for p in dados_partidas ]
    ax.bar(campeoes, kdas, color='orchid')
    ax.set_ylabel("KDA Ratio")
    st.pyplot(fig)
