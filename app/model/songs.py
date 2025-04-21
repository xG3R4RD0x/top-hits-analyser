from app.model.db_config import get_db_connection
from .song import Song


class Songs:
    def __init__(self):
        """Initialize the Tracks class and ensure the table exists."""
        self._create_table()

    @staticmethod
    def _create_table():
        """Create the songs table if it doesn't exist."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            playlist_name TEXT,
            playlist_id INTEGER NOT NULL,
            release_date TEXT,
            artist TEXT NOT NULL,
            album TEXT,
            youtube_url TEXT,
            FOREIGN KEY (playlist_id) REFERENCES playlists(id)
            )
            """
        )
        DB_CONNECTION.commit()
        
    @staticmethod
    def list_songs_from_playlist(playlist_id):
        """Retrieve all songs from a specific playlist as Song objects."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            "SELECT * FROM songs WHERE playlist_id = ?", (playlist_id,)
        )
        rows = cursor.fetchall()
        return [
            Song(
                id=row[0],
                name=row[1],
                playlist_name=row[2],
                playlist_id=row[3],
                release_date=row[4],
                artist=row[5],
                album=row[6],
                youtube_url=row[7],
            )
            for row in rows
        ]

    @staticmethod
    def add_song(song: Song):
        """Add a new song to the database if it doesn't already exist."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        
        # Check if the song already exists
        cursor.execute(
            """
            SELECT COUNT(*) FROM songs
            WHERE name = ? AND artist = ? AND album = ?
            """,
            (song.name, song.artist, song.album),
        )
        if cursor.fetchone()[0] > 0:
            # Song already exists, do not add it again
            return
        
        # Add the song if it doesn't exist
        cursor.execute(
            """
            INSERT INTO songs (name, playlist_name, playlist_id, release_date, artist, album, youtube_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                song.name,
                song.playlist_name,
                song.playlist_id,
                song.release_date,
                song.artist,
                song.album,
                song.youtube_url,
            ),
        )
        DB_CONNECTION.commit()

    @staticmethod
    def get_song(song_id) -> Song:
        """Retrieve a song by its ID."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        row = cursor.fetchone()
        if row:
            return Song(
                id=row[0],
                name=row[1],
                playlist_name=row[2],
                playlist_id=row[3],
                release_date=row[4],
                artist=row[5],
                album=row[6],
                youtube_url=row[7],
            )
        return None

    @staticmethod
    def delete_song(song_id):
        """Delete a song by its ID."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))
        DB_CONNECTION.commit()

    @staticmethod
    def update_song(song: Song):
        """Update a song's details."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            UPDATE songs
            SET name = ?, playlist_name = ?, playlist_id = ?, release_date = ?, artist = ?, album = ?, youtube_url = ?
            WHERE id = ?
        """,
            (
                song.name,
                song.playlist_name,
                song.playlist_id,
                song.release_date,
                song.artist,
                song.album,
                song.youtube_url,
                song.id,
            ),
        )
        DB_CONNECTION.commit()

    @staticmethod
    def list_songs():
        """Retrieve all songs."""
        DB_CONNECTION = get_db_connection()
        cursor = DB_CONNECTION.cursor()
        cursor.execute("SELECT * FROM songs")
        return cursor.fetchall()
