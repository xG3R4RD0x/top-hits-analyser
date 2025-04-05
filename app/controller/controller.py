from tkinter import Tk
from app.view.main_view import MainView
# from app.model.model import DatabaseModel  # Suponiendo que el modelo se llama DatabaseModel

class MainController:
    def __init__(self, root):
        self.root = root
        self.view = MainView(root)
        # self.model = DatabaseModel()  # Instancia del modelo

        # Configurar los comandos de los botones
        self.view.set_button_commands({
            "update_and_download": self.update_and_download,
            "check_database": self.check_database,
            "update_database": self.update_database,
            "download_with_database": self.download_with_database,
            "view_database": self.view_database,
        })

    def update_and_download(self):
        """Actualizar la base de datos y descargar canciones."""
        # self.model.update_database()
        # self.model.download_songs()
        print("Base de datos actualizada y canciones descargadas.")

    def check_database(self):
        """Revisar el estado de la base de datos."""
        # status = self.model.check_database_status()
        print("Estado de la base de datos: Revisando...")

    def update_database(self):
        """Actualizar la base de datos."""
        # self.model.update_database()
        print("Base de datos actualizada.")

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