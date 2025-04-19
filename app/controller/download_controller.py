from app.controller.base_controller import BaseController
import time
import random


class DownloadController(BaseController):
    """Specific controller for the download view"""

    def __init__(self, main_controller):
        super().__init__(main_controller)
        self.stop_download = False

    def register_events(self):
        """Register specific events for the download view"""
        self.view.register_event_handler("navigate_to", self.handle_navigation)
        self.view.register_event_handler("start_download", self.start_download)

    def handle_navigation(self, view_name):
        """Handle navigation events from the view"""
        self.navigate_to(view_name)

    def start_download(self):
        """Start the song download process."""
        print("DownloadController: Starting song download...")
        self.stop_download = False
        self._download_process()

    def _download_process(self):
        """Simulated download process for demonstration"""
        # Get all song rows in the view
        for row_id in self.view.download_rows:
            if self.stop_download:
                break

            # Simulate downloading this song
            self._simulate_download_song(row_id)

    def _simulate_download_song(self, row_id):
        """Simulate downloading a specific song"""
        progress = 0
        statuses = ["Downloading", "Processing", "Completed"]
        current_status = 0

        self.view.update_progress(row_id, progress, statuses[current_status])

        while progress < 100 and not self.stop_download:
            # Simulate random progress
            progress += random.randint(1, 10)
            progress = min(progress, 100)

            # Change status sometimes
            if progress > 50 and current_status == 0:
                current_status = 1

            if progress == 100:
                current_status = 2

            # Update UI
            self.view.update_progress(row_id, progress, statuses[current_status])

            # Wait some time
            time.sleep(0.3)

            # Allow UI to update
            self.view.update()

    def stop_downloads(self):
        """Stop the current download process"""
        self.stop_download = True
        print("DownloadController: Downloads stopped.")
