class Song:
    def __init__(
        self, playlist_name, name, artist, album, release_date, youtube_url=None
    ):
        self.playlist_name = playlist_name
        self.name = name
        self.artist = artist
        self.album = album
        self.release_date = release_date
        self.youtube_url = youtube_url

    def __repr__(self):
        return f"Song({self.playlist_name}, {self.name}, {self.artist}, {self.album}, {self.release_date}, {self.youtube_url})"
