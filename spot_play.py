# Lista playlists públicas de um usuário spotify com suas respectivas tracks. 
# É preciso fornecer url com id do usuário.  
# Limite de 50 playlists.

import requests
from bs4 import BeautifulSoup
import json
import sys

def get_spotify_playlists(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    
    # Obtendo o token de acesso
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    access_token_tag = soup.find('script', {'id':'session'})
    json_obj = json.loads(access_token_tag.get_text())
    access_token_text = json_obj['accessToken']
    
    # Definindo o endpoint da API do Spotify
    user_id = url.split('/')[-2]  # Extrair o ID do usuário a partir do URL
    endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists?limit=50"
    
    # Atualizando os headers com o token de acesso e outros parâmetros necessários
    headers.update({
        "Authorization": f"Bearer {access_token_text}",
        'referer': url,
        'accept': 'application/json',
        'app-platform': 'WebPlayer'
    })
    
    # Fazendo a solicitação à API e obtendo os dados das playlists
    data = requests.get(endpoint, headers=headers).json()
    
    # Extraindo os nomes e IDs das playlists
    playlists_info = [(playlist['name'], playlist['id']) for playlist in data['items']]
    
    return access_token_text, playlists_info

def show_tracks(playlist_id, access_token):
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Fazendo a solicitação à API para obter as faixas da playlist
    data = requests.get(endpoint, headers=headers).json()
    
    
    for i, item in enumerate(data['items'], 1):
        track = item['track']
        print(f"{i}. {track['artists'][0]['name']} - {track['name']}")

# Exemplo de uso:
url = sys.argv[1] 
access_token, playlists = get_spotify_playlists(url)

for name, playlist_id in playlists:
    print(f"Playlist: {name}".upper())
    show_tracks(playlist_id, access_token)
    print()

