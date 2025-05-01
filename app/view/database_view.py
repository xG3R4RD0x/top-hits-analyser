import tkinter as tk
from tkinter import ttk

from app.view.base_view import BaseView


class DatabaseView(BaseView):
    """Vista para mostrar y gestionar la base de datos"""

    def setup_ui(self):
        # Título de la vista
        self.view_label = ttk.Label(self, text="Base de Datos", font=("Helvetica", 14))
        self.view_label.pack(pady=10)

        # Frame para la tabla y controles
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        # Crear un Treeview para mostrar los datos
        self.create_treeview()

        # Botones de acción
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="x", pady=10)

        self.back_button = ttk.Button(
            self.buttons_frame,
            text="Volver al Menú Principal",
            command=self.go_to_main_menu,
        )
        self.back_button.pack(side="left", padx=5)

        self.refresh_button = ttk.Button(
            self.buttons_frame,
            text="Mostrar todas las canciones",
            command=self.fetch_all_songs,
        )
        self.refresh_button.pack(side="right", padx=5)

    def create_treeview(self):
        """Crear un Treeview para mostrar los datos de las canciones"""
        columns = ("playlist", "name", "artist", "album", "release_date", "youtube_url")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        # Definir las cabeceras
        self.tree.heading("playlist", text="Playlist")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("artist", text="Artista")
        self.tree.heading("album", text="Álbum")
        self.tree.heading("release_date", text="Fecha")
        self.tree.heading("youtube_url", text="URL YouTube")

        # Configurar anchos de columnas
        self.tree.column("playlist", width=150)
        self.tree.column("name", width=200)
        self.tree.column("artist", width=200)
        self.tree.column("album", width=150)
        self.tree.column("release_date", width=100)
        self.tree.column("youtube_url", width=250)

        # Agregar scrollbars
        self.vsb = ttk.Scrollbar(
            self.content_frame, orient="vertical", command=self.tree.yview
        )
        self.hsb = ttk.Scrollbar(
            self.content_frame, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        # Posicionar los elementos
        self.tree.grid(column=0, row=0, sticky="nsew")
        self.vsb.grid(column=1, row=0, sticky="ns")
        self.hsb.grid(column=0, row=1, sticky="ew")

        # Configurar el grid para expandirse correctamente
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def fetch_all_songs(self):
        """Actualizar los datos en la vista"""
        self.trigger_event("fetch_all_songs")

    def go_to_main_menu(self):
        """Volver al menú principal"""
        self.trigger_event("navigate_to", "main_menu")

    def add_data(self, songs):
        """Añadir datos al tree view"""
        # Limpiar datos actuales
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Añadir nuevos datos
        for i, song in enumerate(songs):
            self.tree.insert(
                "",
                "end",
                iid=i,
                values=(
                    song.playlist_name,
                    song.name,
                    song.artist,
                    song.album,
                    song.release_date,
                    song.youtube_url,
                ),
            )
