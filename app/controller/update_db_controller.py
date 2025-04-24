from app.controller.base_controller import BaseController
import time
from app.model.playlists import Playlists
from app.model.songs import Songs
from app.model.song import Song


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
        update_porcentage_step= 100/ len(playlists)
        update_porcentage = 0
        if not playlists:
            self.view.add_log_message("No playlists available for update.")
            return

        self.view.add_log_message("Updating songs from playlists...")
        for playlist in playlists:
            self.view.add_log_message(f"Fetching songs from playlist: {playlist[0]}")
            print(playlist)
            playlist_songs_list = self.fetch_songs_from_playlist(playlist[1], playlist[0])
            if  len(playlist_songs_list) == 0:
                continue
            else:
                self.view.add_log_message(f"Adding songs to database...")
            for song in playlist_songs_list:
                self.view.add_log_message(f"{song.artist} - {song.name} (ID: {song.id})")
                Songs.add_song(song)
              
            self.view.add_log_message(f"Songs from playlist {playlist[0]} successfully added.")
            update_porcentage += update_porcentage_step
            self.view.update_progress(update_porcentage)
            
        self.view.update_progress(100)
        
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
                playlist_list.append((playlist.name, playlist.playlist_id, playlist.genre))
            self.view.add_log_message("Playlist information loaded successfully.")
            return playlist_list
            
    def fetch_songs_from_playlist(self, playlist_id, playlist_name):
        """Fetch songs from a specific playlist and return them as a list of Song objects."""
        
        
        # TODO: Esto solo extrae las cosas de la base de datos
        # lo que se necesita es que saque las canciones de la api de spotify y las meta en la base de datos
        # en el handler de la API de spotify se tienen que extraer las canciones por plazylist_id y luego
        # ver si ya existen en la base de datos, si no existen se añaden a la base de datos
    
        songs = self.sp.get_tracks_from_playlist(playlist_id, playlist_name)
        if not songs:
            self.view.add_log_message("No songs found in the playlist")
            return []
        else:
            self.view.add_log_message(f"Found {len(songs)} songs:")
            return songs
 
    def _update_process(self):
        """Simulated update process for demonstration"""
        steps = [
            "Connecting to Spotify API...",
            "Retrieving playlists...",
            "Downloading song information...",
            "Searching YouTube URLs...",
            "Updating database...",
            "Saving results...",
        ]

        progress_per_step = 100 / len(steps)
        current_progress = 0

        for step in steps:
            if self.view.cancelled or self.stop_update:
                break

            self.view.add_log_message(step)
            current_progress += progress_per_step / 2
            self.view.update_progress(current_progress)

            # Simulate processing time
            time.sleep(1)
            # Allow UI to update
            self.view.update()

            # Simulate progress within step
            for i in range(10):
                if self.view.cancelled or self.stop_update:
                    break
                time.sleep(0.1)
                current_progress += progress_per_step / 20
                self.view.update_progress(current_progress)
                # Allow UI to update
                self.view.update()

            self.view.add_log_message(f"✓ {step} completed")

        # Finish operation
        if not self.view.cancelled and not self.stop_update:
            self.view.complete_operation(True)

    def cancel_update_operation(self):
        """Cancel the update operation in progress."""
        print("UpdateDBController: Cancelling update operation...")
        self.view.cancelled = True
        self.stop_update = True
        self.view.complete_operation(False)
