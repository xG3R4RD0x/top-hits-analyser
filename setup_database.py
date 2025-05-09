from app.model.db_config import initialize_db
from app.model.songs import Songs
from app.model.playlists import Playlists   
from init_db import create_database


def setup_database():
    db_name = "tracks.db"
    """Initialize the database and create necessary tables."""
    
    print("Creating the database if not existing...")
    create_database(db_name)
    
    print("Setting up the database...")

    # Initialize the DB connection
    initialize_db(db_name)

    # Create the tables explicitly
    Songs._create_table()
    Playlists._create_table()

    # Update playlists from JSON after table creation
    Playlists.update_playlists_from_json("./playlist_list.json")

    print("Database setup complete. Tables 'playlists' and 'songs' are ready.")


if __name__ == "__main__":
    setup_database()
