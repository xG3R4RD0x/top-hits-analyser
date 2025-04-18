class Playlist:
    def __init__(self, playlist_id, name, genre=None):
        self.playlist_id = playlist_id
        self.name = name
        self.genre = genre

    def to_tuple(self):
        """Convert the playlist object to a tuple for database operations."""
        return self.playlist_id, self.name, self.genre
