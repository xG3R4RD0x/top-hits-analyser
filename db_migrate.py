import sqlite3

def migrate_playlists_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Eliminar la columna 'genre' si tu SQLite es >= 3.35.0
    cursor.execute("ALTER TABLE Playlists DROP COLUMN url;")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_playlists_table("tracks.db")
