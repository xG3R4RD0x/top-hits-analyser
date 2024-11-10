import sqlite3
import os
from song import Song

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


def update_song(song_id, **kwargs):
    """
    Update the details of a song in the database.

    Parameters:
    song_id (int): The ID of the song to update.
    **kwargs: Arbitrary keyword arguments representing the columns to update and their new values.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Crear la parte SET de la consulta SQL dinámicamente
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(song_id)

        cursor.execute(
            f"""
            UPDATE tracks
            SET {set_clause}
            WHERE id = ?
        """,
            values,
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al actualizar la canción: {e}")
    finally:
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


def get_missing_tracks(songs):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear una lista de tuplas (name, artist) para las canciones
    song_tuples = [(song.name, song.artist) for song in songs]

    # Crear una consulta SQL para verificar la existencia de cada canción
    placeholders = ", ".join(["(?, ?)"] * len(song_tuples))
    query = f"""
        SELECT name, artist FROM tracks WHERE (name, artist) IN ({placeholders})
    """

    # Ejecutar la consulta
    cursor.execute(query, [item for sublist in song_tuples for item in sublist])
    existing_tracks = cursor.fetchall()

    # Crear un set de identificadores únicos para los tracks existentes (name, artist)
    existing_track_ids = set(existing_tracks)

    # Filtrar las canciones que no están en la base de datos
    missing_tracks = [
        song for song in songs if (song.name, song.artist) not in existing_track_ids
    ]

    conn.close()
    return missing_tracks


def get_tracks_without_youtube_url():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT playlist_name, name, artist, album, release_date, youtube_url FROM tracks WHERE youtube_url IS NULL
    """
    )
    tracks = cursor.fetchall()

    conn.close()
    return [Song(*track) for track in tracks]


def count_tracks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tracks")
    count = cursor.fetchone()[0]

    conn.close()
    return count
