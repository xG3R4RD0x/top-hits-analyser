import tkinter as tk
from tkinter import ttk

from app.view.base_view import BaseView


class MainMenuView(BaseView):
    """Vista del menú principal"""

    def setup_ui(self):
        # Título de la vista
        self.view_label = ttk.Label(self, text="Menú Principal", font=("Helvetica", 14))
        self.view_label.pack(pady=10)

        # Frame para los botones
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="both", expand=True)

        # Botones
        self.update_and_download_button = ttk.Button(
            self.buttons_frame,
            text="Actualizar base de datos y descargar canciones",
            command=self.update_and_download,
        )
        self.update_and_download_button.pack(fill="x", pady=5)

        self.check_database_button = ttk.Button(
            self.buttons_frame,
            text="Revisar base de datos actual",
            command=self.check_database,
        )
        self.check_database_button.pack(fill="x", pady=5)

        self.update_database_button = ttk.Button(
            self.buttons_frame,
            text="Actualizar base de datos",
            command=self.update_songs_database,
        )
        self.update_database_button.pack(fill="x", pady=5)

        self.download_with_database_button = ttk.Button(
            self.buttons_frame,
            text="Descargar canciones con base de datos actual",
            command=self.download_with_database,
        )
        self.download_with_database_button.pack(fill="x", pady=5)

        self.view_database_button = ttk.Button(
            self.buttons_frame,
            text="Ver base de datos",
            command=self.view_database,
        )
        self.view_database_button.pack(fill="x", pady=5)

    def update_and_download(self):
        """Trigger the 'update_and_download' event."""
        self.trigger_event("update_and_download")

    def check_database(self):
        """Trigger the 'check_database' event."""
        self.trigger_event("check_database")

    def update_songs_database(self):
        """Trigger the 'update_songs_database' event."""
        self.trigger_event("update_songs_database")

    def download_with_database(self):
        """Trigger the 'download_with_database' event."""
        self.trigger_event("download_with_database")

    def view_database(self):
        """Trigger the 'view_database' event."""
        self.trigger_event("view_database")
