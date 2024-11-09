import sqlite3


def insert_song(db_path, playlist_name, name, artist, album, release_date, youtube_url):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO tracks (playlist_name, name, artist, album, release_date, youtube_url) 
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (playlist_name, name, artist, album, release_date, youtube_url),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"El track {artist} - {name} ya existe en la base de datos.")

    conn.close()


def update_song(
    db_path, song_id, playlist_name, name, artist, album, release_date, youtube_url
):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tracks
        SET playlist_name = ?, name = ?, artist = ?, album = ?, release_date = ?, youtube_url = ?
        WHERE id = ?
    """,
        (playlist_name, name, artist, album, release_date, youtube_url, song_id),
    )

    conn.commit()
    conn.close()


def delete_song(db_path, song_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tracks WHERE id = ?", (song_id,))

    conn.commit()
    conn.close()


def list_songs(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tracks")
    tracks = cursor.fetchall()

    conn.close()
    return tracks


def list_songs_by_playlist(db_path, playlist_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tracks WHERE playlist_name = ?", (playlist_name,))
    tracks = cursor.fetchall()

    conn.close()
    return tracks
