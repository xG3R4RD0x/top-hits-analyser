import unittest
from unittest.mock import patch, MagicMock, mock_open
from app.model.playlists import Playlists
from app.model.playlist import Playlist

class TestPlaylists(unittest.TestCase):

    @patch("app.model.playlists.get_db_connection")
    def test_add_playlist_with_object(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        playlist = Playlist("123", "Test Playlist")
        Playlists.add_playlist(playlist=playlist)
        mock_cursor.execute.assert_called_with(
            """
            INSERT INTO playlists (playlist_id, name)
            VALUES (?, ?)
            """,
            ("123", "Test Playlist"),
        )
        mock_conn.commit.assert_called_once()

    @patch("app.model.playlists.get_db_connection")
    def test_add_playlist_with_params(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        Playlists.add_playlist(id="456", name="Another Playlist")
        mock_cursor.execute.assert_called_with(
            """
            INSERT INTO playlists (playlist_id, name)
            VALUES (?, ?)
            """,
            ("456", "Another Playlist"),
        )
        mock_conn.commit.assert_called_once()

    @patch("app.model.playlists.get_db_connection")
    def test_get_playlist_found(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("789", "Found Playlist")

        playlist = Playlists.get_playlist("789")
        self.assertIsInstance(playlist, Playlist)
        self.assertEqual(playlist.playlist_id, "789")
        self.assertEqual(playlist.name, "Found Playlist")
        self.assertTrue(playlist.url.startswith("https://open.spotify.com/playlist/"))

    @patch("app.model.playlists.get_db_connection")
    def test_get_playlist_not_found(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        playlist = Playlists.get_playlist("notfound")
        self.assertIsNone(playlist)

    @patch("app.model.playlists.get_db_connection")
    def test_delete_playlist(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        Playlists.delete_playlist("123")
        mock_cursor.execute.assert_called_with("DELETE FROM playlists WHERE playlist_id = ?", ("123",))
        mock_conn.commit.assert_called_once()

    @patch("app.model.playlists.get_db_connection")
    def test_update_playlist(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        playlist = Playlist("321", "Old Name")
        Playlists.update_playlist(playlist, name="New Name")
        mock_cursor.execute.assert_called()
        args, kwargs = mock_cursor.execute.call_args
        self.assertIn("UPDATE playlists", args[0])
        self.assertIn("SET name = ?", args[0])
        self.assertIn("WHERE playlist_id = ?", args[0])
        self.assertIn("New Name", args[1])

    @patch("app.model.playlists.get_db_connection")
    def test_list_playlists(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ("1", "Playlist 1"),
            ("2", "Playlist 2"),
        ]
        playlists = Playlists.list_playlists()
        self.assertEqual(len(playlists), 2)
        self.assertTrue(all(isinstance(p, Playlist) for p in playlists))

    @patch("app.model.playlists.get_db_connection")
    def test_get_playlist_by_name(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("abc", "ByName")

        playlist = Playlists.get_playlist_by_name("ByName")
        self.assertIsInstance(playlist, Playlist)
        self.assertEqual(playlist.name, "ByName")

    @patch("app.model.playlists.Playlists.get_playlist")
    @patch("app.model.playlists.Playlists.add_playlist")
    @patch("app.model.playlists.Playlists.update_playlist")
    @patch("builtins.open", new_callable=mock_open, read_data='{"playlists":[{"id":"x1","name":"Test"}]}')
    def test_update_playlists_from_json_add(self, mock_file, mock_update, mock_add, mock_get):
        mock_get.return_value = None
        Playlists.update_playlists_from_json("fake.json")
        mock_add.assert_called()
        mock_update.assert_not_called()

    @patch("app.model.playlists.Playlists.get_playlist")
    @patch("app.model.playlists.Playlists.add_playlist")
    @patch("app.model.playlists.Playlists.update_playlist")
    @patch("builtins.open", new_callable=mock_open, read_data='{"playlists":[{"id":"x2","name":"Test2"}]}')
    def test_update_playlists_from_json_update(self, mock_file, mock_update, mock_add, mock_get):
        mock_get.return_value = Playlist("x2", "Test2")
        Playlists.update_playlists_from_json("fake.json")
        mock_update.assert_called()
        mock_add.assert_not_called()

    def test_generate_playlist_url_from_id(self):
        url = Playlists.generate_playlist_url_from_id("abc123")
        self.assertEqual(url, "https://open.spotify.com/playlist/abc123")

if __name__ == "__main__":
    unittest.main()
