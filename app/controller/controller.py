from tkinter import Tk
from app.view.main_view import MainView

# from app.model.model import DatabaseModel  # Suponiendo que el modelo se llama DatabaseModel


class MainController:
    def __init__(self, root):
        self.root = root
        self.view = MainView(root, self)  # Pass the controller to the view

    def navigate_to(self, view_name):
        """
        Navigate to a specific view by name.
        Args:
            view_name: The name of the view to display.
        """
        if view_name not in self.view.frames:
            print(f"Error: View '{view_name}' does not exist.")
            return
        self.view.show_frame(view_name)

    def handle_action(self, action_name):
        """
        Handle actions triggered by views.
        Args:
            action_name: The name of the action to handle.
        """
        actions = {
            "update_and_download": self.update_and_download,
            "check_database": self.check_database,
            "update_songs_database": self.update_songs_database,
            "download_with_database": self.download_with_database,
            "view_database": lambda: self.navigate_to("database_view"),
        }
        if action_name in actions:
            actions[action_name]()

    def update_and_download(self):
        """Actualizar la base de datos y descargar canciones."""
        # self.model.update_database()
        # self.model.download_songs()
        print("Base de datos actualizada y canciones descargadas.")

    def check_database(self):
        """Revisar el estado de la base de datos."""
        # status = self.model.check_database_status()
        print("Estado de la base de datos: Revisando...")

    def update_songs_database(self):
        """Actualizar la base de datos de canciones."""
        # self.model.update_database()
        print("Base de datos actualizadaaa.")

    def download_with_database(self):
        """Descargar canciones usando la base de datos actual."""
        # self.model.download_songs()
        print("Canciones descargadas con la base de datos actual.")

    def view_database(self):
        """Ver el contenido de la base de datos."""
        # data = self.model.get_database_content()
        print("Contenido de la base de datos: Visualizando...")


if __name__ == "__main__":
    root = Tk()
    controller = MainController(root)
    root.mainloop()
