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

    def handle_navigation(self, view_name):
        """Handle navigation events from the view"""
        self.navigate_to(view_name)

    def start_update_process(self):
        """Start the database update process"""
        self.stop_update = False

        self.view.add_log_message("Starting database update process...")
        playlists = self.fetch_playlists()
        update_porcentage_step = 100 / len(playlists)
        update_porcentage = 0
        if not playlists:
            self.view.add_log_message("No playlists available for update.")
            return

        self.view.add_log_message("Updating songs from playlists...")
        for playlist in playlists:
            self.view.add_log_message(f"Fetching songs from playlist: {playlist[0]}")
            print(playlist)
            playlist_songs_list = self.fetch_songs_from_playlist(
                playlist[1], playlist[0]
            )
            if len(playlist_songs_list) == 0:
                continue
            else:
                self.view.add_log_message(f"Adding songs to database...")
            for song in playlist_songs_list:
                self.view.add_log_message(
                    f"{song.artist} - {song.name} (ID: {song.id})"
                )
                Songs.add_song(song)

            self.view.add_log_message(
                f"Songs from playlist {playlist[0]} successfully added."
            )
            update_porcentage += update_porcentage_step
            self.view.update_progress(update_porcentage)

        self.view.complete_operation(True)

        self.view.add_log_message("Database update process completed.")

    def fetch_playlists(self):
        self.view.add_log_message("Retrieving playlists from database...")
        playlists = Playlists.list_playlists()
        if not playlists:
            self.view.add_log_message("No playlists found in the database.")
            return ()
        else:
            self.view.add_log_message(f"Found {len(playlists)} playlists:")
            playlist_list = []
            # Display each playlist in the log messages and collect tuples
            for playlist in playlists:
                playlist_info = (
                    f"Playlist: {playlist.name} (ID: {playlist.playlist_id})"
                )
                if playlist.genre:
                    playlist_info += f", Genre: {playlist.genre}"
                self.view.add_log_message(playlist_info)
                playlist_list.append(
                    (playlist.name, playlist.playlist_id, playlist.genre)
                )
            self.view.add_log_message("Playlist information loaded successfully.")
            return playlist_list

    def fetch_songs_from_playlist(self, playlist_id, playlist_name):
        """Fetch songs from a specific playlist and return them as a list of Song objects."""
        songs = self.sp.get_tracks_from_playlist(playlist_id, playlist_name)
        if not songs:
            self.view.add_log_message("No songs found in the playlist")
            return []
        else:
            self.view.add_log_message(f"Found {len(songs)} songs:")
            return songs

    def fetch_songs_urls(self):
        """Fetch new songs URLs and add them to the database."""

        def process_song(song, lock):
            """Process a single song: fetch its URL and update the database."""
            if self.stop_update:
                return

            self.view.add_log_message(f"Fetching URL for song: {song.name}")
            video_url = Downloader.get_video_url(song)
            if video_url:
                with lock:  # Synchronize database updates
                    if song.youtube_url == video_url:
                        self.view.add_log_message(
                            f"URL already exists for song: {song.name}"
                        )
                    else:
                        song.youtube_url = video_url
                        Songs.update_song(song.id, {"youtube_url": video_url})
                        self.view.add_log_message(f"Updated URL for song: {song.name}")
            else:
                self.view.add_log_message(f"No URL found for song: {song.name}")

        def background_task():
            self.view.add_log_message("Fetching songs URLs from the database...")
            songs = Songs.list_songs()
            total_songs = len(songs)
            if total_songs == 0:
                self.view.add_log_message("No songs found in the database.")
                self.stop_update = True
                self.view.complete_operation(False)
                return

            update_porcentage_step = 100 / total_songs
            update_porcentage = 0
            self.view.add_log_message(f"Found {total_songs} songs in the database.")

            # Lock for synchronizing shared resources
            lock = threading.Lock()

            # Use ThreadPoolExecutor for multithreading
            with ThreadPoolExecutor(
                max_workers=5
            ) as executor:  # Adjust max_workers as needed
                futures = []
                for song in songs:
                    futures.append(executor.submit(process_song, song, lock))

                # Wait for all threads to complete
                for future in futures:
                    future.result()  # Raise exceptions if any occurred in threads

                    # Update progress bar safely
                    with lock:
                        update_porcentage += update_porcentage_step
                        self.view.update_progress(update_porcentage)

            self.view.complete_operation(True)
            self.view.add_log_message("Song URLs fetched successfully.")

        # Start the background task in a new thread
        threading.Thread(target=background_task, daemon=True).start()

    def download_songs(self):
        """Download songs from the database using multithreading without blocking the GUI."""

        def process_song(song, lock):
            """Download a single song."""
            if self.stop_update:
                return

            self.view.add_log_message(f"Downloading song: {song.name}")
            Downloader.download_audio(song)

            # Update progress bar safely
            with lock:
                nonlocal update_porcentage  # Declare as nonlocal to modify the outer variable
                update_porcentage += update_porcentage_step
                self.view.update_progress(update_porcentage)

        def background_task():
            """Background task to download songs."""
            self.view.add_log_message("Downloading songs...")
            songs = Songs.list_songs()
            if not songs:
                self.view.add_log_message("No songs found in the database.")
                self.stop_update = True
                self.view.complete_operation(False)
                return

            total_songs = len(songs)
            nonlocal update_porcentage_step, update_porcentage  # Declare as nonlocal
            update_porcentage_step = 100 / total_songs
            update_porcentage = 0

            # Lock for synchronizing shared resources
            lock = threading.Lock()

            # Use ThreadPoolExecutor for multithreading
            with ThreadPoolExecutor(
                max_workers=5
            ) as executor:  # Adjust max_workers as needed
                futures = [executor.submit(process_song, song, lock) for song in songs]

                # Wait for all threads to complete
                for future in futures:
                    future.result()  # Raise exceptions if any occurred in threads

            self.view.complete_operation(True)
            self.view.add_log_message("Songs downloaded successfully.")

        # Initialize variables in the outer scope
        update_porcentage = 0
        update_porcentage_step = 0

        # Start the background task in a new thread
        threading.Thread(target=background_task, daemon=True).start()

    def cancel_update_operation(self):
        """Cancel the update operation in progress."""
        print("UpdateDBController: Cancelling update operation...")
        self.view.cancelled = True
        self.stop_update = True
        self.view.complete_operation(False)
