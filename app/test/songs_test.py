import unittest
from unittest.mock import patch, MagicMock
from app.model.songs import Songs
from app.model.song import Song


class TestSongs(unittest.TestCase):
    @patch("app.model.songs.get_db_connection")
    def test_list_songs_from_playlist(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Song1", "Playlist1", 1, "2023-01-01", "Artist1", "Album1", "url1"),
            (2, "Song2", "Playlist1", 1, "2023-01-02", "Artist2", "Album2", "url2"),
        ]

        songs = Songs.list_songs_from_playlist(1)
        self.assertEqual(len(songs), 2)
        self.assertEqual(songs[0].name, "Song1")
        self.assertEqual(songs[1].artist, "Artist2")

    @patch("app.model.songs.get_db_connection")
    def test_add_song(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)  # Song does not exist

        song = Song(
            id=None,
            name="New Song",
            playlist_name="Playlist1",
            playlist_id=1,
            release_date="2023-01-01",
            artist="New Artist",
            album="New Album",
            youtube_url="new_url",
        )
        Songs.add_song(song)
        mock_cursor.execute.assert_called_with(
            """
            INSERT INTO songs (name, playlist_name, playlist_id, release_date, artist, album, youtube_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "New Song",
                "Playlist1",
                1,
                "2023-01-01",
                "New Artist",
                "New Album",
                "new_url",
            ),
        )

    @patch("app.model.songs.get_db_connection")
    def test_get_song(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (
            1,
            "Song1",
            "Playlist1",
            1,
            "2023-01-01",
            "Artist1",
            "Album1",
            "url1",
        )

        song = Songs.get_song(1)
        self.assertIsNotNone(song)
        self.assertEqual(song.name, "Song1")
        self.assertEqual(song.artist, "Artist1")

    @patch("app.model.songs.get_db_connection")
    def test_delete_song(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        Songs.delete_song(1)
        mock_cursor.execute.assert_called_with("DELETE FROM songs WHERE id = ?", (1,))

    @patch("app.model.songs.get_db_connection")
    def test_update_song(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        updates = {"name": "Updated Song", "artist": "Updated Artist"}
        Songs.update_song(1, updates)
        mock_cursor.execute.assert_called_with(
            """
            UPDATE songs
            SET name = ?, artist = ?
            WHERE id = ?
            """,
            ["Updated Song", "Updated Artist", 1],
        )

if __name__ == "__main__":
    unittest.main()
