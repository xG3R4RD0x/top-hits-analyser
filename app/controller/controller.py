from tkinter import Tk
from app.view.main_view import MainView
from app.view.menu_view import MainMenuView
from app.view.database_view import DatabaseView
from app.view.download_view import DownloadView
from app.view.update_db_view import UpdateDBView


class MainController:
    def __init__(self, root):
        # Inicializar la vista principal
        self.view = MainView(root)

        # Inicializar todas las vistas/frames necesarios
        self.init_frames()

        # Registrar manejadores de eventos para todas las vistas
        self.register_event_handlers()

    def init_frames(self):
        """Inicializa todos los frames/vistas de la aplicación y los añade al gestor de vistas."""
        # Crear frame para menú principal
        menu_frame = self.view.add_frame(MainMenuView, "main_menu")

        # Crear frame para vista de base de datos
        db_frame = self.view.add_frame(DatabaseView, "database_view")

        # Crear frame para vista de descargas
        download_frame = self.view.add_frame(DownloadView, "download_view")

        # Crear frame para vista de actualización de base de datos
        update_db_frame = self.view.add_frame(UpdateDBView, "update_db_view")

    def register_event_handlers(self):
        """Registra los manejadores de eventos para todas las vistas."""
        # Registrar eventos para el menú principal
        menu = self.view.frames["main_menu"]
        menu.register_event_handler("update_and_download", self.update_and_download)
        menu.register_event_handler("check_database", self.check_database)
        menu.register_event_handler("update_songs_database", self.update_songs_database)
        menu.register_event_handler(
            "download_with_database", self.download_with_database
        )
        menu.register_event_handler("view_database", self.view_database)

        # Registrar eventos para la vista de base de datos
        db_view = self.view.frames["database_view"]
        db_view.register_event_handler("navigate_to", self.navigate_to)
        db_view.register_event_handler("refresh_database", self.refresh_database)

        # Registrar eventos para la vista de descargas
        download_view = self.view.frames["download_view"]
        download_view.register_event_handler("navigate_to", self.navigate_to)
        download_view.register_event_handler("start_download", self.start_download)

        # Registrar eventos para la vista de actualización de base de datos
        update_db_view = self.view.frames["update_db_view"]
        update_db_view.register_event_handler("navigate_to", self.navigate_to)
        update_db_view.register_event_handler(
            "cancel_update_operation", self.cancel_update_operation
        )

    def navigate_to(self, view_name):
        """
        Navigate to a specific view by name.
        Args:
            view_name: The name of the view to display.
        """
        self.view.show_frame(view_name)

    def update_and_download(self):
        """Actualizar la base de datos y descargar canciones."""
        print("Base de datos actualizada y canciones descargadas.")
        # Navegar a la vista de actualización y comenzar el proceso
        self.navigate_to("update_db_view")
        update_view = self.view.frames["update_db_view"]
        update_view.start_operation()
        # Aquí se iniciaría un proceso asíncrono para actualizar la base de datos

    def check_database(self):
        """Revisar el estado de la base de datos."""
        print("Estado de la base de datos: Revisando...")
        # Implementación real: consultar el modelo y mostrar información

    def update_songs_database(self):
        """Actualizar la base de datos de canciones."""
        print("Base de datos actualizándose...")
        self.navigate_to("update_db_view")
        update_view = self.view.frames["update_db_view"]
        update_view.start_operation()
        # Aquí se iniciaría un proceso asíncrono para actualizar la base de datos

    def download_with_database(self):
        """Descargar canciones usando la base de datos actual."""
        print("Canciones descargándose con la base de datos actual.")
        self.navigate_to("download_view")
        # Aquí se iniciaría un proceso asíncrono para descargar las canciones

    def view_database(self):
        """Ver el contenido de la base de datos."""
        print("Mostrando contenido de la base de datos...")
        self.navigate_to("database_view")
        # Aquí se cargarían los datos reales de la base de datos y se mostrarían

    def refresh_database(self):
        """Actualizar los datos mostrados en la vista de base de datos."""
        print("Actualizando datos mostrados...")
        # Implementación real: recargar datos del modelo y actualizar la vista

    def start_download(self):
        """Iniciar el proceso de descarga de canciones."""
        print("Iniciando descarga de canciones...")
        # Implementación real: iniciar proceso de descarga asíncrono

    def cancel_update_operation(self):
        """Cancelar la operación de actualización en curso."""
        print("Cancelando operación de actualización...")
        update_view = self.view.frames["update_db_view"]
        update_view.cancelled = True
        update_view.complete_operation(False)


if __name__ == "__main__":
    root = Tk()
    controller = MainController(root)
    root.mainloop()
