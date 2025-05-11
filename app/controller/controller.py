from tkinter import Tk
from app.view.main_view import MainView
from app.view.menu_view import MainMenuView
from app.view.database_view import DatabaseView
from app.view.update_db_view import UpdateDBView
from app.view.manage_playlists_view import ManagePlaylistsView

# Import specific controllers
from app.controller.menu_controller import MenuController
from app.controller.database_controller import DatabaseController
from app.controller.update_db_controller import UpdateDBController
from app.controller.manage_playlists_controller import ManagePlaylistsController


class MainController:
    def __init__(self, root):
        # Initialize main view
        self.view = MainView(root)

        # Create all frames/views needed for the application
        self.init_frames()

        # Show the initial view (main menu)
        self.navigate_to("main_menu")

    def init_frames(self):
        """Initialize all frames/views of the application and add them to the view manager."""
        # Create frame for main menu with its controller
        menu_controller = MenuController(self)
        menu_frame = self.view.add_frame(MainMenuView, "main_menu", menu_controller)

        # Create frame for database view with its controller
        db_controller = DatabaseController(self)
        db_frame = self.view.add_frame(DatabaseView, "database_view", db_controller)

        # Create frame for database update view with its controller
        update_db_controller = UpdateDBController(self)
        update_db_frame = self.view.add_frame(
            UpdateDBView, "update_db_view", update_db_controller)
            
        manage_playlists_controller = ManagePlaylistsController(self)
        manage_playlists_frame = self.view.add_frame(
            ManagePlaylistsView, "manage_playlists_view", manage_playlists_controller
            
        )

    def navigate_to(self, view_name):
        """
        Navigate to a specific view by name.
        Args:
            view_name: The name of the view to display.
        """
        return self.view.show_frame(view_name)


if __name__ == "__main__":
    root = Tk()
    controller = MainController(root)
    root.mainloop()
