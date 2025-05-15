class Playlist:
    def __init__(self, playlist_id, name, url = None):
        self.playlist_id = playlist_id
        self.name = name
        self.url = url

    def to_tuple(self):
        """Convert the playlist object to a tuple for database operations."""
        return self.playlist_id, self.name, self.url
