import unittest
from unittest.mock import patch, MagicMock
from app.model.downloader import Downloader


class Song:
    """Mock Song class for testing."""

    def __init__(self, artist, name):
        self.artist = artist
        self.name = name


class TestDownloader(unittest.TestCase):
    @patch("app.model.downloader.YoutubeDL")
    def test_get_video_url(self, mock_youtubedl):
        # Arrange
        song = Song(artist="Artist", name="Song")
        mock_ydl_instance = MagicMock()
        mock_youtubedl.return_value.__enter__.return_value = mock_ydl_instance
        mock_ydl_instance.extract_info.return_value = {
            "entries": [{"url": "https://youtube.com/video1"}]
        }
        downloader = Downloader(url="")

        # Act
        video_url = downloader.get_video_url(song)

        # Assert
        self.assertEqual(video_url, "https://youtube.com/video1")
        mock_ydl_instance.extract_info.assert_called_once_with(
            "ytsearch:Artist - Song", download=False
        )

    @patch("app.model.downloader.YoutubeDL")
    @patch("os.makedirs")
    def test_download_audio(self, mock_makedirs, mock_youtubedl):
        # Arrange
        mock_ydl_instance = MagicMock()
        mock_youtubedl.return_value.__enter__.return_value = mock_ydl_instance
        downloader = Downloader(url="https://youtube.com/video1")
        downloader.build_song_title = MagicMock(return_value="Artist - Song")

        # Act
        downloader.download_audio(output_path="test_music")

        # Assert
        mock_makedirs.assert_called_once_with("test_music", exist_ok=True)
        mock_ydl_instance.download.assert_called_once_with(
            ["https://youtube.com/video1"]
        )


if __name__ == "__main__":
    unittest.main()
