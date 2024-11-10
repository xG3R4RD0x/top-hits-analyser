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


class UniqueSongList:

    def __init__(self, songs=None):
        self.songs = []
        self.song_set = set()
        if songs:
            for song in songs:
                self.append(song)

    def append(self, song):
        song_key = (song.name, song.artist)
        if song_key not in self.song_set:
            self.songs.append(song)
            self.song_set.add(song_key)

    def __iter__(self):
        return iter(self.songs)

    def __len__(self):
        return len(self.songs)

    def __repr__(self):
        return f"UniqueSongList({self.songs})"
