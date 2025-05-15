from app.controller.base_controller import BaseController


class MenuController(BaseController):
    """Specific controller for the main menu view"""

    def register_events(self):
        """Register specific events for the menu view"""
        self.view.register_event_handler(
            "update_and_download", self.update_and_download
        )
        self.view.register_event_handler("view_database", self.view_database)
        self.view.register_event_handler("manage_playlists", self.manage_playlists)

    def update_and_download(self):
        """Update the database and download songs."""
        print("MenuController: Database updated and songs downloaded.")
        self.navigate_to("update_db_view")
        update_view = self.main_controller.view.frames["update_db_view"]

    def update_playlists(self):
        """Update Playlists."""
        print("Updating playlits...")
        self.navigate_to("update_playlists_view")
        # Real implementation: query the model and display information

    def view_database(self):
        """View database content."""
        print("MenuController: Showing database content...")
        self.navigate_to("database_view")
        
    def manage_playlists(self):
        """Manage playlists."""
        print("MenuController: Managing playlists...")
        self.navigate_to("manage_playlists_view")
