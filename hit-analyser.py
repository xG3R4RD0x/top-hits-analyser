import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from get_music import YouTubeAudioDownloader
from search_songs import YouTubeSearcher


class SpotifyPlaylistAnalyzer:

    playlists = {
        "Mansion Reggaeton": "37i9dQZF1DWZjqjZMudx9T",
        "Reggaeton 2024": "03sDEv7FN58Mb9CJOs1Tgn",
        # Agrega más playlists según sea necesario
    }

    def __init__(self):
        load_dotenv()
        self.CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.client_credentials_manager = SpotifyClientCredentials(
            client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET
        )
        self.sp = spotipy.Spotify(
            client_credentials_manager=self.client_credentials_manager
        )

    def get_tracks_from_playlist(self, playlist_id, playlist_name, limit=100):
        tracks = []
        results = self.sp.playlist_tracks(playlist_id, limit=limit)
        for item in results["items"]:
            track = item["track"]
            track_info = {
                "playlist_name": playlist_name,
                "name": track["name"],
                "artist": ", ".join(artist["name"] for artist in track["artists"]),
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
            }
            tracks.append(track_info)
        return tracks

    def save_to_excel(self, tracks, filename="playlist_tracks.xlsx"):
        df = pd.DataFrame(
            tracks,
            columns=[
                "playlist_name",
                "name",
                "artist",
                "album",
                "release_date",
                "YouTube URL",
            ],
        )
        df.to_excel(filename, index=False)
        print("exportado al excel")


def main():

    while True:
        action = input(
            "¿Qué quieres hacer? (1: Actualizar Lista de canciones, 2: Descargar Canciones desde la Lista, 3: Actualizar Lista y descargar canciones): "
        )

        analyzer = SpotifyPlaylistAnalyzer()
        if action == "1":

            all_tracks = []
            unique_tracks = set()

            for playlist_name, playlist_id in analyzer.playlists.items():
                try:
                    tracks = analyzer.get_tracks_from_playlist(
                        playlist_id, playlist_name
                    )
                    for track in tracks:
                        track_key = (track["name"], track["artist"])
                        if track_key not in unique_tracks:
                            unique_tracks.add(track_key)
                            all_tracks.append(track)
                except Exception as e:
                    print(f"Error al obtener las canciones para {playlist_name}: {e}")

            all_tracks = YouTubeSearcher.add_youtube_urls_to_tracks(all_tracks)
            analyzer.save_to_excel(all_tracks)

        elif action == "2":
            tracks = YouTubeAudioDownloader.read_songs_from_file(
                "./playlist_tracks.xlsx"
            )
            downloader = YouTubeAudioDownloader(tracks)
            downloader.download_songs()

        elif action == "3":
            all_tracks = []
            unique_tracks = set()

            for playlist_name, playlist_id in analyzer.playlists.items():
                try:
                    tracks = analyzer.get_tracks_from_playlist(
                        playlist_id, playlist_name
                    )
                    for track in tracks:
                        track_key = (track["name"], track["artist"])
                        if track_key not in unique_tracks:
                            unique_tracks.add(track_key)
                            all_tracks.append(track)
                except Exception as e:
                    print(f"Error al obtener las canciones para {playlist_name}: {e}")

            all_tracks = YouTubeSearcher.add_youtube_urls_to_tracks(all_tracks)
            analyzer.save_to_excel(all_tracks)

            downloader = YouTubeAudioDownloader(all_tracks)
            downloader.download_songs()

        elif action == "q":
            break

        else:
            print("Comando no valido, prueba de nuevo")
    SystemExit


if __name__ == "__main__":
    main()
