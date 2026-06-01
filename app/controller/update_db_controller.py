from app.controller.base_controller import BaseController
from app.model.playlists import Playlists
from app.model.songs import Songs
from app.model.downloader import Downloader
import threading
from concurrent.futures import ThreadPoolExecutor


class UpdateDBController(BaseController):
    """Specific controller for the database update view"""

    def __init__(self, main_controller):
        super().__init__(main_controller)
        self.stop_update = False

    def register_events(self):
        """Register specific events for the database update view"""
        self.view.register_event_handler("navigate_to", self.handle_navigation)
        self.view.register_event_handler(
            "cancel_update_operation", self.cancel_update_operation
        )
        self.view.register_event_handler("start_update", self.start_update_process)
        self.view.register_event_handler("fetch_urls", self.fetch_songs_urls)
        self.view.register_event_handler("download_songs", self.download_songs)
        self.view.register_event_handler("fetch_playlist_songs", self.fetch_playlist_songs)

    def handle_navigation(self, view_name):
        """Handle navigation events from the view"""
        self.navigate_to(view_name)

    def update_view(self):
        """Load playlists (names only, songs lazy-loaded on expand)"""
        playlists = Playlists.list_playlists()
        if not playlists:
            self.view.add_log_message("No playlists found in database.")
            self.view.load_playlists([])
            return
        data = [(pl, []) for pl in playlists]
        self.view.load_playlists(data)

    def fetch_playlist_songs(self, playlist_id):
        return Songs.list_songs_from_playlist(playlist_id)

    def start_update_process(self, selected_playlist_ids):
        """Update only the selected playlists"""
        self.stop_update = False
        self.view.add_log_message("Starting database update process...")

        if not selected_playlist_ids:
            self.view.add_log_message("No playlists selected for update.")
            self.view.complete_operation(False)
            return

        update_porcentage_step = max(1, 100 / len(selected_playlist_ids))
        update_porcentage = 0

        for playlist_id in selected_playlist_ids:
            if self.stop_update:
                break

            playlist = Playlists.get_playlist(playlist_id)
            if not playlist:
                self.view.add_log_message(f"Playlist {playlist_id} not found, skipping.")
                continue

            self.view.add_log_message(f"Fetching songs from playlist: {playlist.name}")
            playlist_songs_list = self.fetch_songs_from_playlist(
                playlist_id, playlist.name
            )

            if not playlist_songs_list:
                self.view.add_log_message(f"No songs found in {playlist.name}")
                continue

            song_ids_in_playlist = []
            for song in playlist_songs_list:
                Songs.add_song(song)
                song_ids_in_playlist.append(song.id)

            Songs.mark_songs_active_in_playlist(playlist_id)
            Songs.mark_songs_inactive_in_playlist(playlist_id, song_ids_in_playlist)

            self.view.add_log_message(
                f"Songs from playlist {playlist.name} successfully updated."
            )
            update_porcentage += update_porcentage_step
            self.view.update_progress(update_porcentage)

        self.view.complete_operation(True)
        self.view.add_log_message("Database update process completed.")
        self.update_view()

    def fetch_songs_from_playlist(self, playlist_id, playlist_name):
        """Fetch songs from a specific Spotify playlist."""
        songs = self.sp.get_tracks_from_playlist(playlist_id, playlist_name)
        if not songs:
            self.view.add_log_message("No songs found in the playlist")
            return []
        else:
            self.view.add_log_message(f"Found {len(songs)} songs:")
            return songs

    def fetch_songs_urls(self, selected_song_ids):
        """Fetch YouTube URLs for selected songs only."""
        def process_song(song, lock):
            if self.stop_update:
                return
            self.view.add_log_message(f"Fetching URL for song: {song.name}")
            video_url = Downloader.get_video_url(song)
            if video_url:
                with lock:
                    if song.youtube_url == video_url:
                        self.view.add_log_message(f"URL already exists for song: {song.name}")
                    else:
                        song.youtube_url = video_url
                        Songs.update_song(song.id, {"youtube_url": video_url})
                        self.view.add_log_message(f"Updated URL for song: {song.name}")
            else:
                self.view.add_log_message(f"No URL found for song: {song.name}")

        def background_task():
            self.view.add_log_message("Fetching songs URLs...")
            songs = Songs.list_songs()
            total = len(songs)
            if total == 0:
                self.view.add_log_message("No songs in database.")
                self.stop_update = True
                self.view.complete_operation(False)
                return

            # Filter to only selected songs
            selected_set = set(selected_song_ids)
            songs_to_process = [s for s in songs if s.id in selected_set]
            if not songs_to_process:
                self.view.add_log_message("No selected songs to process.")
                self.view.complete_operation(False)
                return

            self.view.add_log_message(f"Processing {len(songs_to_process)} selected songs...")
            update_porcentage_step = 100 / len(songs_to_process)
            update_porcentage = 0
            lock = threading.Lock()

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(process_song, song, lock)
                    for song in songs_to_process
                ]
                for future in futures:
                    future.result()
                    with lock:
                        update_porcentage += update_porcentage_step
                        self.view.update_progress(update_porcentage)

            self.view.complete_operation(True)
            self.view.add_log_message("URL fetch completed.")

        threading.Thread(target=background_task, daemon=True).start()

    def download_songs(self, selected_song_ids):
        """Download selected songs only."""
        self.view.add_log_message("Preparing to download songs...")
        self.check_downloaded_songs(selected_song_ids)
        self.view.update_progress(0)

        def process_song(song, lock):
            if self.stop_update:
                return
            self.view.add_log_message(f"Downloading song: {song.name}")
            Downloader.download_audio(song)
            with lock:
                nonlocal update_porcentage
                update_porcentage += update_porcentage_step
                self.view.update_progress(update_porcentage)

        def background_task():
            self.view.add_log_message("Downloading selected songs...")

            # Filter selected songs
            selected_set = set(selected_song_ids)
            all_songs = Songs.list_songs()
            songs_to_download = [s for s in all_songs if s.id in selected_set and not s.downloaded]

            if not songs_to_download:
                self.view.add_log_message("No selected songs pending download.")
                self.stop_update = True
                self.view.complete_operation(False)
                return

            total = len(songs_to_download)
            nonlocal update_porcentage_step, update_porcentage
            update_porcentage_step = 100 / total
            update_porcentage = 0
            lock = threading.Lock()

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(process_song, song, lock)
                    for song in songs_to_download
                ]
                for future in futures:
                    future.result()

            self.view.complete_operation(True)
            self.view.add_log_message("Download completed.")

        update_porcentage = 0
        update_porcentage_step = 0
        threading.Thread(target=background_task, daemon=True).start()

    def cancel_update_operation(self):
        """Cancel the update operation in progress."""
        print("UpdateDBController: Cancelling update operation...")
        self.view.cancelled = True
        self.stop_update = True
        self.view.complete_operation(False)

    def check_downloaded_songs(self, song_ids=None):
        """Check which songs are already downloaded."""
        self.view.add_log_message("Checking downloaded songs...")
        songs = Songs.list_songs()
        if not songs:
            return

        if song_ids:
            selected_set = set(song_ids)
            songs = [s for s in songs if s.id in selected_set]

        total_songs = len(songs)
        if total_songs == 0:
            return

        update_percentage_step = 100 / total_songs
        update_percentage = 0

        for song in songs:
            if self.stop_update:
                break
            try:
                exists = Downloader.check_if_exists(song)
            except Exception as e:
                self.view.add_log_message(f"Error checking '{song.name}': {e}")
                continue
            if exists:
                Songs.mark_as_downloaded(song.id)
                song.downloaded = True
            else:
                Songs.mark_as_not_downloaded(song.id)
                song.downloaded = False
            update_percentage += update_percentage_step
            self.view.update_progress(update_percentage)
