from app.controller.base_controller import BaseController
from app.model.songs import Songs


class DatabaseController(BaseController):
    """Specific controller for the database view"""

    def register_events(self):
        """Register specific events for the database view"""
        self.view.register_event_handler("navigate_to", self.handle_navigation)
        self.view.register_event_handler("fetch_all_songs", self.fetch_all_songs)

    def handle_navigation(self, view_name):
        """Handle navigation events from the view"""
        self.navigate_to(view_name)

    def fetch_all_songs(self):
        """Update the data displayed in the database view."""
        print("DatabaseController: Updating displayed data...")
        songs = Songs.list_songs()

        self.view.add_data(songs)
