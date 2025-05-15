import os
import re
import json
import spotipy
from app.model.song import Song
from app.model.playlist import Playlist
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
        """Fetch tracks from a playlist and return them as Song objects."""
        tracks = []
        print(str(limit))
        try:
            print(f"Fetching tracks from playlist: {playlist_id}")
            results = self.sp.playlist_items(
                playlist_id,
                limit=limit,
                fields="items(track(id,name,artists(name),album(name,release_date))),next",
            )

            while results:
                for item in results["items"]:
                    track = item["track"]
                    if track:  # Ensure the track object is not None
                        if not track["name"] or not track["artists"]:
                            print(
                                f"Skipping track with missing or invalid name or artists: {track}"
                            )
                            continue
                        track_info = Song(
                            id=track["id"],
                            playlist_name=playlist_name,
                            playlist_id=playlist_id,
                            name=self.sanitize_songname(track["name"]),
                            artist=self.sanitize_songname(
                                ", ".join(artist["name"] for artist in track["artists"])
                            ),
                            album=track["album"]["name"],
                            release_date=track["album"]["release_date"],
                        )
                        tracks.append(track_info)

                # Check if there is a next page
                if results["next"]:
                    results = self.sp.next(results)
                else:
                    break
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error fetching tracks from playlist {playlist_id}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
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
        
    def get_playlist_metadata_from_url(self, url):
        """Extract playlist ID and name from a Spotify URL.
        
        fields for playlist:
        https://developer.spotify.com/documentation/web-api/reference/get-playlist
        
        """
        try:
                playlist_id = self.get_id_from_url(url)
                print(f"Extracted playlist ID: {playlist_id}")
              
                metadata = self.sp.playlist(
                playlist_id, 
                fields="id,name"
            )           
                
                id= metadata["id"]
                name = metadata["name"]
                
                return id, name
            
        except Exception as e:
            print(f"Error extracting metadata from URL: {e}")
            return None, None


    def get_id_from_url(self, url):
        """Extract playlist ID from a Spotify URL."""
        try:
            match = re.search(r"playlist/([^?]+)", url)
            if match:
                playlist_id = match.group(1)  # Extract the playlist ID
                return playlist_id
            else:
                print("No playlist ID found in the URL.")
                return None
        except Exception as e:
            print(f"Error extracting ID from URL: {e}")
            return None

    def sanitize_songname(self, name: str) -> str:
        illegal_chars_pattern = r'[\/:*?"<>|\\-]'
        sanitized_songname = re.sub(illegal_chars_pattern, " ", name)
        sanitized_songname = re.sub(" +", " ", sanitized_songname)
        sanitized_songname = sanitized_songname.strip().strip(".")
        return sanitized_songname
