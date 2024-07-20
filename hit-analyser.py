import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()

# Credenciales de la API de Spotify
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

# Autenticación y obtención del token de acceso
auth_url = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(auth_url, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# Convertir la respuesta a JSON
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

# Crear una instancia del cliente de Spotify
sp = spotipy.Spotify(auth=access_token)

# Función para obtener las canciones más populares de un género en un país específico
def get_top_tracks_by_genre_and_country(genre, country, limit=10):
    # Obtener la categoría de género
    categories = sp.categories(country=country, limit=50)
    genre_category = None
    for category in categories['categories']['items']:
        if genre.lower() in category['name'].lower():
            genre_category = category['id']
            break
    
    if not genre_category:
        return f"No se encontró la categoría de género '{genre}' en el país '{country}'."

    # Obtener listas de reproducción de la categoría de género
    playlists = sp.category_playlists(category_id=genre_category, country=country, limit=10)
    top_tracks = []

    for playlist in playlists['playlists']['items']:
        # Obtener las pistas de la lista de reproducción
        tracks = sp.playlist_tracks(playlist['id'], limit=limit)
        for track in tracks['items']:
            track_info = {
                'name': track['track']['name'],
                'artist': track['track']['artists'][0]['name'],
                'album': track['track']['album']['name'],
                'release_date': track['track']['album']['release_date']
            }
            top_tracks.append(track_info)
    
    return top_tracks

# Ejemplo de uso
genre = 'pop'
country = 'US'
top_tracks = get_top_tracks_by_genre_and_country(genre, country)

for idx, track in enumerate(top_tracks, 1):
    print(f"{idx}. {track['name']} by {track['artist']} (Album: {track['album']}, Release Date: {track['release_date']})")
