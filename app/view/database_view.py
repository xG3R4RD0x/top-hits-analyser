import tkinter as tk
from tkinter import ttk

from app.view.base_view import BaseView


class DatabaseView(BaseView):
    """Vista para mostrar y gestionar la base de datos con filtros"""

    def setup_ui(self):
        # Frame superior para controles/filtros
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.pack(fill="x", padx=10, pady=10)

        # Search box
        search_label = ttk.Label(self.controls_frame, text="Search (Song/Artist):")
        search_label.pack(side="left", padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.apply_filters())
        self.search_entry = ttk.Entry(self.controls_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side="left", padx=(0, 15))

        # Playlist filter
        playlist_label = ttk.Label(self.controls_frame, text="Playlist:")
        playlist_label.pack(side="left", padx=(0, 5))
        
        self.playlist_var = tk.StringVar(value="All")
        self.playlist_combo = ttk.Combobox(
            self.controls_frame, 
            textvariable=self.playlist_var, 
            width=15, 
            state="readonly"
        )
        self.playlist_combo.pack(side="left", padx=(0, 15))
        self.playlist_combo.bind("<<ComboboxSelected>>", lambda *args: self.apply_filters())

        # Artist filter
        artist_label = ttk.Label(self.controls_frame, text="Artist:")
        artist_label.pack(side="left", padx=(0, 5))
        
        self.artist_var = tk.StringVar(value="All")
        self.artist_combo = ttk.Combobox(
            self.controls_frame, 
            textvariable=self.artist_var, 
            width=15, 
            state="readonly"
        )
        self.artist_combo.pack(side="left", padx=(0, 15))
        self.artist_combo.bind("<<ComboboxSelected>>", lambda *args: self.apply_filters())

        # Reset filters button
        self.reset_button = ttk.Button(
            self.controls_frame,
            text="Reset Filters",
            command=self.reset_filters,
        )
        self.reset_button.pack(side="left", padx=5)

        # Frame para la tabla
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        # Crear Treeview con columnas
        self.create_treeview()

        # Store all songs for filtering
        self.all_songs = []
        self.filtered_songs = []

    def create_treeview(self):
        """Crear un Treeview para mostrar los datos de las canciones"""
        columns = ("playlist", "name", "artist", "album", "release_date", "youtube_url", "in_playlist")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)

        # Definir las cabeceras
        self.tree.heading("playlist", text="Playlist")
        self.tree.heading("name", text="Song Name")
        self.tree.heading("artist", text="Artist")
        self.tree.heading("album", text="Album")
        self.tree.heading("release_date", text="Release Date")
        self.tree.heading("youtube_url", text="YouTube URL")
        self.tree.heading("in_playlist", text="Active")

        # Configurar anchos de columnas
        self.tree.column("playlist", width=120)
        self.tree.column("name", width=180)
        self.tree.column("artist", width=150)
        self.tree.column("album", width=130)
        self.tree.column("release_date", width=90)
        self.tree.column("youtube_url", width=150, anchor="center")
        self.tree.column("in_playlist", width=60, anchor="center")

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

        # Define styling for rows
        self.tree.tag_configure("inactive", background="#d3d3d3")

    def fetch_all_songs(self):
        """Actualizar los datos en la vista"""
        self.trigger_event("fetch_all_songs")

    def apply_filters(self):
        """Apply search and filter criteria"""
        search_text = self.search_var.get().lower()
        playlist_filter = self.playlist_var.get()
        artist_filter = self.artist_var.get()

        self.filtered_songs = []

        for song in self.all_songs:
            # Check search (Song Name + Artist)
            if search_text:
                if search_text not in song.name.lower() and search_text not in song.artist.lower():
                    continue

            # Check playlist filter
            if playlist_filter != "All":
                if song.playlist_name != playlist_filter:
                    continue

            # Check artist filter
            if artist_filter != "All":
                if song.artist != artist_filter:
                    continue

            self.filtered_songs.append(song)

        self.display_songs(self.filtered_songs)

    def reset_filters(self):
        """Reset all filters to default"""
        self.search_var.set("")
        self.playlist_var.set("All")
        self.artist_var.set("All")
        self.apply_filters()

    def add_data(self, songs):
        """Añadir datos al tree view"""
        self.all_songs = songs
        
        # Update playlist combobox
        playlists = ["All"] + sorted(list(set(song.playlist_name for song in songs)))
        self.playlist_combo["values"] = playlists
        
        # Update artist combobox
        artists = ["All"] + sorted(list(set(song.artist for song in songs)))
        self.artist_combo["values"] = artists

        # Apply current filters
        self.apply_filters()

    def display_songs(self, songs):
        """Display songs in treeview with proper styling"""
        # Limpiar datos actuales
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Añadir nuevos datos
        for i, song in enumerate(songs):
            in_playlist_text = "Yes" if song.in_playlist else "No"
            tags = ("inactive",) if not song.in_playlist else ()
            
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
                    song.youtube_url if song.youtube_url else "-",
                    in_playlist_text,
                ),
                tags=tags,
            )
