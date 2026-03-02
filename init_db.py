import sqlite3


def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_name TEXT NOT NULL,
            name TEXT NOT NULL,
            artist TEXT NOT NULL,
            album TEXT,
            release_date TEXT,
            youtube_url TEXT,
            downloaded BOOLEAN,
            UNIQUE(artist, name)
        )
        """
    )

    conn.commit()
    conn.close()


# Crear la base de datos y las tablas
create_database("tracks.db")
