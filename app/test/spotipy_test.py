import unittest
from app.api.spotipy import SpotifyAPIHandler
from app.model.song import Song


class TestSpotifyAPIHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the SpotifyAPIHandler instance for testing."""
        cls.spotify_handler = SpotifyAPIHandler()

    def test_get_tracks_from_playlist(self):
        """Test the get_tracks_from_playlist function."""
        print("\nTesting get_tracks_from_playlist...")
        playlist_id = "6PH7Dt6RC8R3CZJseARXue"
        playlist_name = "REGGAETON ECUADOR"
        tracks = self.spotify_handler.get_tracks_from_playlist(
            playlist_id, playlist_name, limit=5
        )
        # print(f"Tracks retrieved: {tracks}")
        print(f"Tracks retrieved: {str(len(tracks))}")
        self.assertIsInstance(tracks, list)
        for track in tracks:
            self.assertIsInstance(track, Song)

        self.assertGreater(len(tracks), 0)

    # def test_read_playlist_ids(self):
    #     """Test the read_playlist_ids function."""
    #     print("\nTesting read_playlist_ids...")
    #     json_file_path = "playlists.json"  # Replace with the path to your JSON file
    #     playlists = self.spotify_handler.read_playlist_ids(json_file_path)
    #     print(f"Playlists retrieved: {playlists}")
    #     self.assertIsInstance(playlists, dict)
    #     self.assertGreater(len(playlists), 0)

    # def test_sanitize_songname(self):
    #     """Test the sanitize_songname function."""
    #     print("\nTesting sanitize_songname...")
    #     song_name = "Test: Song/Name*?"
    #     sanitized_name = self.spotify_handler.sanitize_songname(song_name)
    #     print(f"Original: {song_name} | Sanitized: {sanitized_name}")
    #     self.assertNotIn("/", sanitized_name)
    #     self.assertNotIn(":", sanitized_name)
    #     self.assertNotIn("*", sanitized_name)
    #     self.assertNotIn("?", sanitized_name)


if __name__ == "__main__":
    unittest.main()
