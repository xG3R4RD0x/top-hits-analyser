from yt_dlp import YoutubeDL
import os
from app.model.song import Song
from app.model.songs import Songs


class Downloader:
    def __init__(self):
        pass

    # 2. Function to download the audio of the song from the URL
    @staticmethod
    def build_song_title(song):
        """Builds the title of the song from a Song object."""
        return f"{song.artist} - {song.name}"

    @staticmethod
    def get_video_url(song, overwrite=False):
        """Searches YouTube for the song and retrieves the video URL."""
        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
            "extract_flat": True,
        }
        if not overwrite and song.youtube_url:
            return song.youtube_url

        query = Downloader.build_song_title(song)
        with YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(f"ytsearch:{query}", download=False)
                if "entries" in result and len(result["entries"]) > 0:

                    return result["entries"][0]["url"]
            except Exception as e:
                print(f"Error searching YouTube for {query}: {e}")
        return None

    @staticmethod
    def download_audio(song: Song, output_path="music/hits"):
        """Downloads the audio of the song from the URL."""

        if song is None:
            print("The song object cannot be None.")
            return
        # checks if the output path exists, if not creates it
        os.makedirs(output_path, exist_ok=True)
        video_url = song.youtube_url

        video_title = Downloader.build_song_title(song)

        if not video_url:
            print(f"Could not find a video URL for {video_title}")
            return

        # Check if the file already exists in the output path
        output_file = os.path.join(output_path, f"{video_title}.mp3")
        if os.path.exists(output_file):
            print(f"The file '{output_file}' already exists. Skipping download.")
            return

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(output_path, f"{video_title}.%(ext)s"),
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading audio for: {video_title}")
                ydl.download([video_url])
                Downloader.check_if_exists(song)

        except Exception as e:
            print(f"Error downloading audio for {video_title}: {e}")

    def check_if_exists(song: Song):
        """Check if the song file already exists in the output path."""
        output_path = "music/hits"
        video_title = Downloader.build_song_title(song)
        output_file = os.path.join(output_path, f"{video_title}.mp3")

        if os.path.exists(output_file):
            Songs.mark_as_downloaded(song.id)
            return True
        return False
