import sqlite3
import os

# Define la ruta a la base de datos en el directorio raíz del proyecto
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tracks.db")


def insert_song(song):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO tracks (playlist_name, name, artist, album, release_date, youtube_url) 
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                song["playlist_name"],
                song["name"],
                song["artist"],
                song["album"],
                song["release_date"],
                song["youtube_url"],
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(
            f"El track {song['artist']} - {song['name']} ya existe en la base de datos."
        )

    conn.close()


def insert_songs_bulk(songs):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.executemany(
            """
            INSERT INTO tracks (playlist_name, name, artist, album, release_date, youtube_url) 
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            [
                (
                    song["playlist_name"],
                    song["name"],
                    song["artist"],
                    song["album"],
                    song["release_date"],
                    song["youtube_url"],
                )
                for song in songs
            ],
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error al insertar canciones: {e}")

    conn.close()


def update_song(song_id, song):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tracks
        SET playlist_name = ?, name = ?, artist = ?, album = ?, release_date = ?, youtube_url = ?
        WHERE id = ?
    """,
        (
            song["playlist_name"],
            song["name"],
            song["artist"],
            song["album"],
            song["release_date"],
            song["youtube_url"],
            song_id,
        ),
    )

    conn.commit()
    conn.close()


def list_songs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tracks")
    tracks = cursor.fetchall()

    conn.close()
    return tracks


def list_songs_by_playlist(playlist_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tracks WHERE playlist_name = ?", (playlist_name,))
    tracks = cursor.fetchall()

    conn.close()
    return tracks


def delete_song(song_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tracks WHERE id = ?", (song_id,))

    conn.commit()
    conn.close()
