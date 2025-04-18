from app.model.tracks import Tracks
from app.model.playlists import Playlists


def setup_database():
    """Initialize the database and create necessary tables."""
    print("Setting up the database...")

    # Initialize Tracks and Playlists to create their respective tables
    Tracks()
    Playlists()

    print("Database setup complete. Tables 'playlists' and 'songs' are ready.")


if __name__ == "__main__":
    setup_database()
