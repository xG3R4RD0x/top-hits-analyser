import sqlite3


def migrate_playlists_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("ALTER TABLE Songs ADD COLUMN downloaded BOOLEAN;")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    migrate_playlists_table("tracks.db")
