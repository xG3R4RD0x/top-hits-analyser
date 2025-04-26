from yt_dlp import YoutubeDL


class Downloader:
    def __init__(self, url: str):
        self.url = url

    # 1. Function to get the URL of the music video from a song
    # 2. Function to download the audio of the song from the URL

    def build_song_title(self, song):
        """Builds the title of the song from a Song object."""
        return f"{song.artist} - {song.name}"

    def get_video_url(self, song):
        """Searches YouTube for the song and retrieves the video URL."""
        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
            "extract_flat": True,
        }

        query = self.build_song_title(song)
        with YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(f"ytsearch:{query}", download=False)
                if "entries" in result and len(result["entries"]) > 0:
                    print(result)
                    return result["entries"][0]["url"]
            except Exception as e:
                print(f"Error searching YouTube for {query}: {e}")
        return None

    def download_audio(self, output_path="music/hits"):
        """Downloads the audio of the song from the URL."""
        import os
        from yt_dlp import YoutubeDL

        os.makedirs(output_path, exist_ok=True)
        video_url = self.url
        video_title = self.build_song_title(self)

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
        except Exception as e:
            print(f"Error downloading audio for {video_title}: {e}")
