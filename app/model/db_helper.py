import sqlite3
from .song import Song  # Import the Song class


class DBHelper:
    def __init__(self, db_name="tracks.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        """Create the songs table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
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
            conn.commit()

    def add_song(self, song: Song):
        """Add a new song to the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tracks (name, playlist_name, release_date, artist, album, youtube_url)
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
            conn.commit()

    def get_song(self, song_id) -> Song:
        """Retrieve a song by its ID."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tracks WHERE id = ?", (song_id,))
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

    def delete_song(self, song_id):
        """Delete a song by its ID."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tracks WHERE id = ?", (song_id,))
            conn.commit()

    def update_song(self, song: Song):
        """Update a song's details."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tracks
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
            conn.commit()
