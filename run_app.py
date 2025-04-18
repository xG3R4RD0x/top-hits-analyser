from tkinter import Tk
from app.controller.controller import MainController
from app.view.menu_view import MainMenuView  # Import MainMenuView
import sqlite3

# Global database connection
DB_CONNECTION = sqlite3.connect("tracks.db", check_same_thread=False)


def close_connection():
    """Close the global database connection."""
    if DB_CONNECTION:
        DB_CONNECTION.close()


def main():
    """
    Entry point for the application.
    Initializes the main controller and starts the Tkinter main loop.
    """
    root = Tk()
    controller = MainController(root)
    controller.view.add_frame(
        MainMenuView, "main_menu"
    )  # Correctly reference MainMenuView
    controller.navigate_to("main_menu")  # Start with the main menu
    root.mainloop()


if __name__ == "__main__":
    main()
