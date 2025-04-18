class Song:
    def __init__(
        self,
        id=None,
        playlist_name=None,
        name=None,
        artist=None,
        album=None,
        release_date=None,
        youtube_url=None,
    ):
        self.id = id
        self.playlist_name = playlist_name
        self.name = name
        self.artist = artist
        self.album = album
        self.release_date = release_date
        self.youtube_url = youtube_url

    def __repr__(self):
        return f"Song(id={self.id}, playlist_name={self.playlist_name}, name='{self.name}', artist='{self.artist}', album='{self.album}', release_date={self.release_date})"
