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

        self.view_database_button = ttk.Button(
            self.buttons_frame,
            text="Ver base de datos",
            command=self.view_database,
        )
        self.view_database_button.pack(fill="x", pady=5)

        self.update_playlists_button = ttk.Button(
            self.buttons_frame,
            text="Actualizar playlists",
            command=self.update_playlists,
        )
        self.update_playlists_button.pack(fill="x", pady=5)

    def update_and_download(self):
        """Trigger the 'update_and_download' event."""
        self.trigger_event("update_and_download")

    def view_database(self):
        """Trigger the 'view_database' event."""
        self.trigger_event("view_database")

    def update_playlists(self):
        """Trigger the 'update_playlists' event."""
        self.trigger_event("update_playlists")
