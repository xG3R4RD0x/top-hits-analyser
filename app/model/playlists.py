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
    def add_playlist(playlist=None, id=None, name=None):
        """
        Add a new playlist to the database.
        Puedes pasar un objeto Playlist, o los parámetros id, name, genre.
        Hay que pasar en el parametro el nombre dle parametro 
        
        
        """
        if playlist is not None and isinstance(playlist, Playlist):
            obj = playlist
        elif id is not None and name is not None:
            obj = Playlist(playlist_id=id, name=name)
        else:
            raise ValueError("Debes pasar un objeto Playlist o los parámetros id y name.")

        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            INSERT INTO playlists (playlist_id, name)
            VALUES (?, ?)
            """,
            (obj.playlist_id, obj.name),    
        )
        DB_CONNECTION.commit()

    @staticmethod
    def get_playlist(playlist_id) -> Playlist:
        """Retrieve a playlist by its playlist_id."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            "SELECT playlist_id, name FROM playlists WHERE playlist_id = ?",
            (playlist_id,),
        )
        row = cursor.fetchone()
        if row:
            return Playlist(playlist_id=row[0], name=row[1], url= Playlists.generate_playlist_url_from_id(row[0]))
        return None
    
    @staticmethod
    def get_playlist_by_name(name) -> Playlist:
        """Retrieve a playlist by its name."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            "SELECT playlist_id, name FROM playlists WHERE name = ?",
            (name,),
        )
        row = cursor.fetchone()
        if row:
            return Playlist(playlist_id=row[0], name=row[1], url=Playlists.generate_playlist_url_from_id(row[0]))
        return None

    @staticmethod
    def delete_playlist(playlist_id):
        """Delete a playlist by its playlist_id."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute("DELETE FROM playlists WHERE playlist_id = ?", (playlist_id,))
        DB_CONNECTION.commit()

    @staticmethod
    def update_playlist(playlist: Playlist = None, **kwargs):
        """
        Update a playlist's details.
        Puedes pasar un objeto Playlist y/o campos a actualizar como argumentos nombrados.
        El registro a actualizar se selecciona usando el playlist_id del objeto playlist.
        Si en kwargs viene un nuevo playlist_id, también se actualizará en la base de datos.
        """
        if playlist is None:
            raise ValueError("Debes pasar una playlist a actualizar")

        if not kwargs:
            raise ValueError("Debes pasar al menos un campo a actualizar")

        # Prepare fields to update
        fields = {}
        if "name" in kwargs:
            fields["name"] = kwargs["name"]
        if "playlist_id" in kwargs:
            fields["playlist_id"] = kwargs["playlist_id"]
            
        # Remove None values
        fields = {k: v for k, v in fields.items() if v is not None}

        if not fields:
            raise ValueError("No hay campos para actualizar.")

        set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
        values = list(fields.values())
     
        values.append(playlist.playlist_id)

        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            f"""
            UPDATE playlists
            SET {set_clause}
            WHERE playlist_id = ?
            """,
            values,
        )
        DB_CONNECTION.commit()

    @staticmethod
    def list_playlists():
        """Retrieve all playlists."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute("SELECT playlist_id, name FROM playlists")
        rows = cursor.fetchall()
        return [Playlist(playlist_id=row[0], name=row[1], url= Playlists.generate_playlist_url_from_id(row[0])) for row in rows]

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
               
            )

            existing_playlist = Playlists.get_playlist(playlist.playlist_id)
            if existing_playlist:
                Playlists.update_playlist(playlist)
            else:
                Playlists.add_playlist(playlist)
    @staticmethod           
    def generate_playlist_url_from_id(playlist_id):
        """Generate a Spotify URL from a playlist ID."""
        return f"https://open.spotify.com/playlist/{playlist_id}"
