from app.controller.base_controller import BaseController


class MenuController(BaseController):
    """Specific controller for the main menu view"""

    def register_events(self):
        """Register specific events for the menu view"""
        self.view.register_event_handler(
            "update_and_download", self.update_and_download
        )
        self.view.register_event_handler("check_database", self.check_database)
        self.view.register_event_handler(
            "update_songs_database", self.update_songs_database
        )

        self.view.register_event_handler("view_database", self.view_database)

    def update_and_download(self):
        """Update the database and download songs."""
        print("MenuController: Database updated and songs downloaded.")
        self.navigate_to("update_db_view")
        update_view = self.main_controller.view.frames["update_db_view"]
        # update_controller = update_view.controller
        # update_controller.start_update_process()

    def check_database(self):
        """Check the database status."""
        print("MenuController: Database status: Checking...")
        # Real implementation: query the model and display information

    def update_songs_database(self):
        """Update the songs database."""
        print("MenuController: Database updating...")
        print("MenuController: Holaaa")

        self.navigate_to("update_db_view")
        # update_view = self.main_controller.view.frames["update_db_view"]

    def view_database(self):
        """View database content."""
        print("MenuController: Showing database content...")
        self.navigate_to("database_view")
