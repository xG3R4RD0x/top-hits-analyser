class Song:
    def __init__(
        self,
        id=None,
        playlist_name=None,
        playlist_id=None,
        name=None,
        artist=None,
        album=None,
        release_date=None,
        youtube_url=None,
        downloaded=None,
    ):
        self.id = id
        self.playlist_name = playlist_name
        self.playlist_id = playlist_id
        self.name = name
        self.artist = artist
        self.album = album
        self.release_date = release_date
        self.youtube_url = youtube_url
        self.downloaded = downloaded

    def __iter__(self):
        """Make the object iterable by returning an iterator over its attributes."""
        return iter(
            {
                "id": self.id,
                "playlist_name": self.playlist_name,
                "playlist_id": self.playlist_id,
                "name": self.name,
                "artist": self.artist,
                "album": self.album,
                "release_date": self.release_date,
                "youtube_url": self.youtube_url,
                "downloaded": self.downloaded,
            }.items()
        )

    def __repr__(self):
        return f"Song(id={self.id}, playlist_name={self.playlist_name}, playlist_id={self.playlist_id}, name='{self.name}', artist='{self.artist}', album='{self.album}', release_date={self.release_date}, downloaded={self.downloaded})"
