from tkinter import Tk
from app.controller.controller import MainController
import sqlite3

# Global database connection
DB_CONNECTION = sqlite3.connect("app_data.db", check_same_thread=False)


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
    root.mainloop()


if __name__ == "__main__":
    main()
