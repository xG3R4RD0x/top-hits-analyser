import sqlite3


def migrate_playlists_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check existing columns
    cursor.execute("PRAGMA table_info(songs)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add downloaded column if it doesn't exist
    if "downloaded" not in columns:
        cursor.execute("ALTER TABLE songs ADD COLUMN downloaded BOOLEAN;")
        conn.commit()
        print("[OK] Added downloaded column to songs table")
    else:
        print("[OK] downloaded column already exists")
    
    # Add in_playlist column if it doesn't exist
    if "in_playlist" not in columns:
        cursor.execute("ALTER TABLE songs ADD COLUMN in_playlist BOOLEAN DEFAULT 0;")
        conn.commit()
        print("[OK] Added in_playlist column to songs table")
    else:
        print("[OK] in_playlist column already exists")

    conn.close()


if __name__ == "__main__":
    migrate_playlists_table("tracks.db")
