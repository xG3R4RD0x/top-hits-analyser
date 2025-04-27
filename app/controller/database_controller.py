from app.controller.base_controller import BaseController


class DatabaseController(BaseController):
    """Specific controller for the database view"""

    def register_events(self):
        """Register specific events for the database view"""
        self.view.register_event_handler("navigate_to", self.handle_navigation)
        self.view.register_event_handler("refresh_database", self.refresh_database)

    def handle_navigation(self, view_name):
        """Handle navigation events from the view"""
        self.navigate_to(view_name)

    def refresh_database(self):
        """Update the data displayed in the database view."""
        print("DatabaseController: Updating displayed data...")
        # Real implementation: reload data from model and update view

        # As an example, we could load sample data
        sample_data = [
            (
                "Top Hits 2023",
                "Gasolina",
                "Daddy Yankee",
                "Barrio Fino",
                "2004-07-13",
                "https://youtube.com/...",
            ),
            (
                "Latin Hits",
                "Despacito",
                "Luis Fonsi",
                "Vida",
                "2017-01-13",
                "https://youtube.com/...",
            ),
            (
                "Reggaeton",
                "Mi Gente",
                "J Balvin",
                "Vibras",
                "2017-06-30",
                "https://youtube.com/...",
            ),
        ]
        self.view.add_data(sample_data)
