from run_app import DB_CONNECTION
from .playlist import Playlist


class Playlists:
    @staticmethod
    def _create_table():
        """Create the playlists table if it doesn't exist."""
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                genre TEXT
            )
        """
        )
        DB_CONNECTION.commit()

    @staticmethod
    def add_playlist(playlist: Playlist):
        """Add a new playlist to the database."""
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            INSERT INTO playlists (playlist_id, name, genre)
            VALUES (?, ?, ?)
        """,
            playlist.to_tuple(),
        )
        DB_CONNECTION.commit()

    @staticmethod
    def get_playlist(playlist_id) -> Playlist:
        """Retrieve a playlist by its playlist_id."""
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
        cursor = DB_CONNECTION.cursor()
        cursor.execute("DELETE FROM playlists WHERE playlist_id = ?", (playlist_id,))
        DB_CONNECTION.commit()

    @staticmethod
    def update_playlist(playlist: Playlist):
        """Update a playlist's details."""
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
        cursor = DB_CONNECTION.cursor()
        cursor.execute("SELECT playlist_id, name, genre FROM playlists")
        rows = cursor.fetchall()
        return [Playlist(playlist_id=row[0], name=row[1], genre=row[2]) for row in rows]
