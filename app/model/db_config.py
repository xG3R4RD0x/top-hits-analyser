import sqlite3

# Initialize the database connection
DB_CONNECTION = None


def initialize_db(db_path="tracks.db"):
    """Initialize the database connection."""
    global DB_CONNECTION
    DB_CONNECTION = sqlite3.connect(db_path, check_same_thread=False)
    return DB_CONNECTION


def get_db_connection():
    """Get the database connection."""
    global DB_CONNECTION
    if DB_CONNECTION is None:
        DB_CONNECTION = initialize_db()
    return DB_CONNECTION
