import requests
import json
import os


def GetPuuid(nome, tag, api_key):
    url = (
        f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nome}/{tag}"
        f"?api_key={api_key}"
    )

    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        puuid = dados["puuid"]
        return puuid
    else:
        print(f"Erro {resposta.status_code}: {resposta.text}")
        return None


def GetSummoner(puuid, api_key):
    url = f"https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
    resposta = requests.get(url)

    if resposta.status_code == 200:

        return resposta.json()

    else:
        print(f"Erro {resposta.status_code}: {resposta.text}")
        return None


def GetMatchIds(puuid, api_key, count=5):
    url = (
        f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        f"?start=0&count={count}&api_key={api_key}"
    )

    resposta = requests.get(url)

    if resposta.status_code == 200:
        return resposta.json()  # lista de match IDs
    else:
        print(f"Erro {resposta.status_code}: {resposta.text}")
        return None

def GetMatchData(match_id, api_key):
    url = (
        f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
        f"?api_key={api_key}"
    )

    resposta = requests.get(url)

    if resposta.status_code == 200:
        return resposta.json()
    else:
        print(f"Erro {resposta.status_code}: {resposta.text}")
        return None

def salvar_json_em_arquivo(dados, nome_arquivo):

    pasta = os.path.dirname(nome_arquivo)
    if not os.path.exists(pasta) and pasta != "":
        os.makedirs(pasta)


    with open(nome_arquivo, "w") as f:
        json.dump(dados, f, indent=4)



