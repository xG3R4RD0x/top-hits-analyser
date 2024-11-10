import os
import spotipy
import pandas as pd
import re
import json
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from get_music import YouTubeAudioDownloader
from search_songs import YouTubeSearcher
from song import Song, UniqueSongList
import db_utils as db


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
            try:
                track = item["track"]
                song = Song(
                    playlist_name=playlist_name,
                    name=self.sanitize_songname(track["name"]),
                    artist=self.sanitize_songname(
                        ", ".join(artist["name"] for artist in track["artists"])
                    ),
                    album=track["album"]["name"],
                    release_date=track["album"]["release_date"],
                )
                print(song.name)

            except Exception as e:
                print(f"Error al procesar la canción: {e}")
            tracks.append(song)
        return tracks

    def save_to_excel(self, tracks, filename="playlist_tracks.xlsx"):
        df = pd.DataFrame(
            [track.to_dict() for track in tracks],
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

    def sanitize_songname(self, name: str) -> str:

        illegal_chars_pattern = r'[\/:*?"<>|\\-]'

        sanitized_songname = re.sub(illegal_chars_pattern, " ", name)

        sanitized_songname = re.sub(" +", " ", sanitized_songname)

        sanitized_songname = sanitized_songname.strip().strip(".")

        return sanitized_songname


def main():

    while True:
        action = input(
            "¿Qué quieres hacer? (1: Actualizar Lista de canciones, 2: Descargar Canciones desde la Lista, 3: Actualizar Lista y descargar canciones, 4: tester de funciones): "
        )

        analyzer = SpotifyPlaylistAnalyzer()
        if action == "1":

            for playlist_name, playlist_id in analyzer.playlists.items():
                try:
                    tracks = analyzer.get_tracks_from_playlist(
                        playlist_id, playlist_name
                    )
                    missing_tracks = db.get_missing_tracks(tracks)
                    db.insert_songs_bulk(missing_tracks)
                except Exception as e:
                    print(f"Error al obtener las canciones para {playlist_name}: {e}")

            new_tracks = db.get_tracks_without_youtube_url()
            print("nuevos tracks: ", len(new_tracks))
            print(
                "cantidad total de canciones en la base de datos: " + db.count_tracks()
            )
            all_tracks = YouTubeSearcher.add_youtube_urls_to_tracks(new_tracks)
            print("Links a youtube agregados")

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
                        track_key = (track.name, track.artist)
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

        elif action == "4":
            print("tester action")
            song_list_from_db = db.list_songs_as_song_objects()
            all_tracks = UniqueSongList(song_list_from_db)
            original_len = len(all_tracks.songs)
            for playlist_name, playlist_id in analyzer.playlists.items():

                try:
                    tracks = analyzer.get_tracks_from_playlist(
                        playlist_id, playlist_name
                    )
                    actual_len = len(all_tracks.songs)
                    for track in tracks:
                        all_tracks.append(track)
                    new_len = len(all_tracks.songs)
                except Exception as e:
                    print(f"Error al obtener las canciones para {playlist_name}: {e}")
                print(
                    f"Se agregaron {new_len-actual_len} canciones de la lista {playlist_name}"
                )
            db.insert_songs_bulk(all_tracks.songs)
            print(
                "se agregaron ",
                len(all_tracks.songs) - original_len,
                " canciones a la base de datos",
            )

        elif action == "q":
            break

        else:
            print("Comando no valido, prueba de nuevo")
    SystemExit


if __name__ == "__main__":
    main()
