from run_app import DB_CONNECTION
from .song import Song


class Tracks:
    @staticmethod
    def _create_table():
        """Create the songs table if it doesn't exist."""
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                playlist_name TEXT NOT NULL,
                release_date TEXT,
                artist TEXT NOT NULL,
                album TEXT,
                youtube_url TEXT
            )
        """
        )
        DB_CONNECTION.commit()

    @staticmethod
    def add_song(song: Song):
        """Add a new song to the database."""
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            INSERT INTO songs (name, playlist_name, release_date, artist, album, youtube_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                song.name,
                song.playlist_name,
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
        cursor = DB_CONNECTION.cursor()
        cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        row = cursor.fetchone()
        if row:
            return Song(
                id=row[0],
                name=row[1],
                playlist_name=row[2],
                release_date=row[3],
                artist=row[4],
                album=row[5],
                youtube_url=row[6],
            )
        return None

    @staticmethod
    def delete_song(song_id):
        """Delete a song by its ID."""
        cursor = DB_CONNECTION.cursor()
        cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))
        DB_CONNECTION.commit()

    @staticmethod
    def update_song(song: Song):
        """Update a song's details."""
        cursor = DB_CONNECTION.cursor()
        cursor.execute(
            """
            UPDATE songs
            SET name = ?, playlist_name = ?, release_date = ?, artist = ?, album = ?, youtube_url = ?
            WHERE id = ?
        """,
            (
                song.name,
                song.playlist_name,
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
        cursor = DB_CONNECTION.cursor()
        cursor.execute("SELECT * FROM songs")
        return cursor.fetchall()
