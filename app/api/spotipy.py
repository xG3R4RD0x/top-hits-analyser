import os
import re
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv


class SpotifyAPIHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpotifyAPIHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            load_dotenv()
            self.CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
            self.CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
            self.client_credentials_manager = SpotifyClientCredentials(
                client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(
                client_credentials_manager=self.client_credentials_manager
            )
            self._initialized = True

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

    def read_playlist_ids(self, json_file_path):
        try:
            with open(json_file_path, "r") as file:
                data = json.load(file)
                playlist = {
                    playlist["name"]: playlist["id"] for playlist in data["playlists"]
                }
                return playlist
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return []

    def sanitize_songname(self, name: str) -> str:
        illegal_chars_pattern = r'[\/:*?"<>|\\-]'
        sanitized_songname = re.sub(illegal_chars_pattern, " ", name)
        sanitized_songname = re.sub(" +", " ", sanitized_songname)
        sanitized_songname = sanitized_songname.strip().strip(".")
        return sanitized_songname
