import os
import spotipy
import pandas as pd
import re
import json
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from get_music import YouTubeAudioDownloader
from search_songs import YouTubeSearcher


class SpotifyPlaylistAnalyzer:

    excelFile_path = "./playlist_tracks.xlsx"

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

        self.playlists = self.read_playlist_ids("./playlist_list.json")

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
            track_info["name"] = self.sanitize_songname(track_info["name"])
            track_info["artist"] = self.sanitize_songname(track_info["artist"])
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

    def read_playlist_ids(self, json_file_path):
        try:
            with open(json_file_path, "r") as file:
                data = json.load(file)
                playlist = {
                    playlist["name"]: playlist["id"] for playlist in data["playlists"]
                }
                return playlist
        except Exception as e:
            print(f"Error al leer el archivo JSON: {e}")
            return []

    def filter_new_and_missing_url_tracks(
        self, new_tracks, existing_file=excelFile_path
    ):
        try:
            # Leer el archivo Excel existente
            df_existing = pd.read_excel(existing_file)

            # Convertir el DataFrame en una lista de diccionarios
            existing_tracks = df_existing.to_dict(orient="records")

            # Crear un set de identificadores únicos para los tracks existentes (nombre y artista)
            existing_track_ids = set(
                (
                    self.sanitize_songname(track["name"]),
                    self.sanitize_songname(track["artist"]),
                )
                for track in existing_tracks
                if pd.notna(
                    track["YouTube URL"]
                )  # Solo incluir tracks que ya tienen URL de YouTube
            )

            # Inicializar una lista para almacenar los tracks filtrados
            filtered_tracks = [
                track
                for track in new_tracks
                if (
                    self.sanitize_songname(track["name"]),
                    self.sanitize_songname(track["artist"]),
                )
                not in existing_track_ids
            ]
            print("tracks nuevos sin url: ", len(filtered_tracks))
            return filtered_tracks

        except Exception as e:
            print(f"No se pudo procesar el Excel: {e}")
            return new_tracks  # En caso de error, devolver todos los nuevos tracks

    def sanitize_songname(self, name: str) -> str:

        illegal_chars_pattern = r'[\/:*?"<>|\\-]'

        sanitized_songname = re.sub(illegal_chars_pattern, " ", name)

        sanitized_songname = re.sub(" +", " ", sanitized_songname)

        sanitized_songname = sanitized_songname.strip().strip(".")

        return sanitized_songname


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
            all_tracks = analyzer.filter_new_and_missing_url_tracks(all_tracks)
            print("tracks totales: ", len(all_tracks))
            all_tracks = YouTubeSearcher.add_youtube_urls_to_tracks(all_tracks)
            analyzer.save_to_excel(all_tracks)

        elif action == "2":
            tracks = YouTubeAudioDownloader.read_songs_from_file(
                analyzer.excelFile_path
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

            all_tracks = analyzer.filter_new_and_missing_url_tracks(all_tracks)
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
