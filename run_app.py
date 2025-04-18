from tkinter import Tk
from app.controller.controller import MainController


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
