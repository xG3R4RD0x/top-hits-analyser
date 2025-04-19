from app.controller.base_controller import BaseController
import time
from app.model.model import DatabaseModel as db


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
        self.view.add_log_message("Retrieving playlists from database...")

        playlists = db.show_playlists(self)

        if not playlists:
            self.view.add_log_message("No playlists found in the database.")
        else:
            self.view.add_log_message(f"Found {len(playlists)} playlists:")

            # Display each playlist in the log messages
            for playlist in playlists:
                playlist_info = (
                    f"Playlist: {playlist.name} (ID: {playlist.playlist_id})"
                )
                if playlist.genre:
                    playlist_info += f", Genre: {playlist.genre}"
                self.view.add_log_message(playlist_info)

        self.view.add_log_message("Playlist information loaded successfully.")

        # self.view.start_operation()
        # self._update_process()

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
