import unittest
from app.model.downloader import Downloader
from app.model.song import Song
from app.model.songs import Songs
from app.model.playlists import Playlists
import os


class TestDownloader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a test song for the class."""
        cls.test_song = cls.get_test_song()

    @classmethod
    def get_test_song(cls):
        """Get a test song."""
        playlists = Playlists.list_playlists()
        if not playlists:
            raise ValueError("No playlists available.")

        first_playlist = playlists[1]
        songs = Songs.list_songs_from_playlist(first_playlist.playlist_id)
        if not songs:
            raise ValueError("No songs available in the first playlist.")
        return songs[0]

    def test_get_video_url(self):
        video_url = Downloader.get_video_url(self.test_song)

        self.assertIsNotNone(video_url)
        self.assertTrue(video_url.startswith("http"))
        self.assertTrue("youtube.com" in video_url)

    def test_download_audio(self):
        """Test the download_audio function."""
        print("\nTesting download_audio...")
        song = self.test_song
        video_url = Downloader.get_video_url(song)
        Songs.update_song(self.test_song.id, {"youtube_url": video_url})
        song = Songs.get_song(self.test_song.id)
        print(f"Song: {song}")
        Downloader.download_audio(song, output_path="download_test")
        print(f"Audio file path: ./download_test/{song.artist} - {song.name}.mp3")
        audio_file_path = f"./download_test/{song.artist} - {song.name}.mp3"
        self.assertTrue(os.path.exists(audio_file_path))


if __name__ == "__main__":
    unittest.main()
