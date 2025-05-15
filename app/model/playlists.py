from app.model.db_config import get_db_connection
from app.model.playlist import Playlist
import json


class Playlists:
    def __init__(self):
        """Initialize the Playlists class and ensure the table exists."""
        self._create_table()

    @staticmethod
    def _create_table():
        """Create the playlists table if it doesn't exist."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS playlists (
            playlist_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
           
            )
            """
        )
        DB_CONNECTION.commit()

    @staticmethod
    def add_playlist(playlist=None, id=None, name=None, genre=None):
        """
        Add a new playlist to the database.
        Puedes pasar un objeto Playlist, o los parámetros id, name, genre.
        Hay que pasar en el parametro el nombre dle parametro 
        
        
        """
        if playlist is not None and isinstance(playlist, Playlist):
            obj = playlist
        elif id is not None and name is not None:
            obj = Playlist(playlist_id=id, name=name, genre=genre)
        else:
            raise ValueError("Debes pasar un objeto Playlist o los parámetros id y name.")

        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            INSERT INTO playlists (playlist_id, name, genre)
            VALUES (?, ?, ?)
            """,
            obj.to_tuple(),
        )
        DB_CONNECTION.commit()

    @staticmethod
    def get_playlist(playlist_id) -> Playlist:
        """Retrieve a playlist by its playlist_id."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            "SELECT playlist_id, name, genre FROM playlists WHERE playlist_id = ?",
            (playlist_id,),
        )
        row = cursor.fetchone()
        if row:
            return Playlist(playlist_id=row[0], name=row[1], genre=row[2])
        return None

    @staticmethod
    def delete_playlist(playlist_id):
        """Delete a playlist by its playlist_id."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute("DELETE FROM playlists WHERE playlist_id = ?", (playlist_id,))
        DB_CONNECTION.commit()

    @staticmethod
    def update_playlist(playlist: Playlist):
        """Update a playlist's details."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            UPDATE playlists
            SET name = ?, genre = ?
            WHERE playlist_id = ?
        """,
            (playlist.name, playlist.genre, playlist.playlist_id),
        )
        DB_CONNECTION.commit()

    @staticmethod
    def list_playlists():
        """Retrieve all playlists."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute("SELECT playlist_id, name, genre FROM playlists")
        rows = cursor.fetchall()
        return [Playlist(playlist_id=row[0], name=row[1], genre=row[2]) for row in rows]

    @staticmethod
    def update_playlists_from_json(json_file_path):
        """Update playlists from a JSON file."""
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Handle the case when playlists are inside a "playlists" key
        if "playlists" in data:
            playlists_data = data["playlists"]
        else:
            playlists_data = data

        if isinstance(playlists_data, dict):
            playlists_data = [playlists_data]

        for playlist_data in playlists_data:
            # Map "id" to "playlist_id" if needed
            playlist_id = playlist_data.get("playlist_id", playlist_data.get("id"))

            playlist = Playlist(
                playlist_id=playlist_id,
                name=playlist_data["name"],
                genre=playlist_data.get("genre"),
            )

            existing_playlist = Playlists.get_playlist(playlist.playlist_id)
            if existing_playlist:
                Playlists.update_playlist(playlist)
            else:
                Playlists.add_playlist(playlist)
