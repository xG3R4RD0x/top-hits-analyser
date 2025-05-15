import tkinter as tk
from tkinter import ttk

from app.view.base_view import BaseView
from app.model.playlists import Playlists
from app.model.playlist import Playlist


class ManagePlaylistsView(BaseView):
    """View to display playlists"""

    def setup_ui(self):
        # View title
        self.view_label = ttk.Label(
            self, text="Manage Playlists", font=("Helvetica", 14)
        )
        self.view_label.pack(pady=0)

        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Playlists management section
        self.playlists_section = ttk.Frame(self.main_frame)
        self.playlists_section.pack(fill="both", expand=True, pady=10)

        # Playlists LabelFrame (debajo del botón y arriba del formulario)
        self.playlists_frame = ttk.LabelFrame(self.playlists_section, text="Current Playlists")
        self.playlists_frame.pack(fill="both", expand=True, pady=0)

        # Toolbar with add button
        self.toolbar_frame = ttk.Frame(self.playlists_frame)
        self.toolbar_frame.pack(fill="x", padx=5, pady=5)

        self.add_button = ttk.Button(
            self.toolbar_frame, 
            text="+ Add Playlist", 
            command=self.add_playlist
        )
        self.add_button.pack(side="left", padx=5)

        # Playlists treeview
        self.playlists_tree = ttk.Treeview(
            self.playlists_frame,
            columns=("name", "edit", "delete"),
            show="headings",
            selectmode="browse"
        )
        
        # Define columns
        self.playlists_tree.heading("name", text="Playlist Name")
        self.playlists_tree.heading("edit", text="Edit")
        self.playlists_tree.heading("delete", text="Delete")
        
        # Column widths
        self.playlists_tree.column("name", width=200, anchor="w")
        self.playlists_tree.column("edit", width=20, anchor="center")
        self.playlists_tree.column("delete", width=20, anchor="center")
          
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.playlists_frame, 
            orient="vertical", 
            command=self.playlists_tree.yview
        )
        self.playlists_tree.configure(yscrollcommand=scrollbar.set)
        
        # Place treeview and scrollbar
        self.playlists_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=5)
        
        # Bind actions to edit and delete buttons
        self.playlists_tree.bind("<Double-1>", self.on_item_double_click)

        # --- Bottom controls: Add/Edit Playlist Form (siempre visible) ---
        self.bottom_controls_frame = ttk.Frame(self.playlists_section)
        self.bottom_controls_frame.pack(fill="x", padx=5, pady=(10, 2))

        # Contenedor principal del formulario (siempre visible, en columna)
        self.form_frame = ttk.Frame(self.bottom_controls_frame)
        self.form_frame.pack(fill="x", expand=True)

        # Contenedor para los campos del formulario (en columna)
        self.form_fields_frame = ttk.Frame(self.form_frame)
        self.form_fields_frame.pack(fill="x", side="top", expand=True)
        self.form_fields_frame.grid_columnconfigure(1, weight=1)
        self.form_fields_frame.grid_columnconfigure(2, weight=0)

        self.url_label = ttk.Label(self.form_fields_frame, text="URL:")
        self.url_label.grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.url_entry = ttk.Entry(self.form_fields_frame)
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        self.extract_button = ttk.Button(
            self.form_fields_frame,
            text="Extraer datos desde url",
            command=self.extract_data_from_url
        )
        self.extract_button.grid(row=0, column=2, sticky="w", padx=2, pady=2)

        ttk.Label(self.form_fields_frame, text="ID:").grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.id_entry = ttk.Entry(self.form_fields_frame)
        self.id_entry.grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        ttk.Label(self.form_fields_frame, text="Nombre:").grid(row=2, column=0, sticky="w", padx=2, pady=2)
        self.name_entry = ttk.Entry(self.form_fields_frame)
        self.name_entry.grid(row=2, column=1, sticky="ew", padx=2, pady=2)

        # Contenedor para los botones (horizontal: volver | guardar/cancelar)
        self.form_actions_frame = ttk.Frame(self.form_frame)
        # No empacar aquí, se hace dinámicamente en show/hide

        self.back_button = ttk.Button(self.form_actions_frame, text="Back to Main Menu", command=self.go_to_main_menu)
        self.back_button.pack(side="left", padx=2)

        self.form_buttons_inner_frame = ttk.Frame(self.form_actions_frame)
        self.form_buttons_inner_frame.pack(side="left", padx=10)

        self.save_button = ttk.Button(self.form_buttons_inner_frame, text="Guardar", command=self.save_new_playlist)
        self.save_button.pack(side="left", padx=2)
        self.cancel_button = ttk.Button(self.form_buttons_inner_frame, text="Cancelar", command=self.hide_add_form)
        self.cancel_button.pack(side="left", padx=2)

        # --- Contenedor de confirmación de borrado (inicialmente oculto) ---
        self.delete_confirm_frame = ttk.Frame(self.form_frame)
        self.delete_confirm_label = ttk.Label(
            self.delete_confirm_frame,
            text="¿Seguro quieres borrar esta playlist?",
            foreground="red"
        )
        self.delete_confirm_label.pack(side="top", pady=5, padx=5)
        self.delete_confirm_buttons = ttk.Frame(self.delete_confirm_frame)
        self.delete_confirm_buttons.pack(side="top", pady=2)
        self.delete_confirm_yes = ttk.Button(
            self.delete_confirm_buttons,
            text="Seguir",
            command=self.confirm_delete_playlist
        )
        self.delete_confirm_yes.pack(side="left", padx=5)
        self.delete_confirm_cancel = ttk.Button(
            self.delete_confirm_buttons,
            text="Cancelar",
            command=self.hide_delete_confirm
        )
        self.delete_confirm_cancel.pack(side="left", padx=5)
        self.delete_confirm_frame.pack_forget()

        # El botón de volver SIEMPRE visible debajo del formulario
        self.back_button_alone = ttk.Button(self.form_frame, text="Back to Main Menu", command=self.go_to_main_menu)
        self.back_button_alone.pack(side="left", padx=2)

        # El formulario inicia oculto (solo oculta campos y botones guardar/cancelar, pero NO el botón volver solo)
        self.form_fields_frame.pack_forget()
        self.form_actions_frame.pack_forget()
        self.delete_confirm_frame.pack_forget()

    def go_to_main_menu(self):
        """Go back to main menu"""
        self.trigger_event("navigate_to", "main_menu")
        
    def load_playlists(self, playlists):
        """Load playlists into the treeview"""
        # Clear existing items
        for item in self.playlists_tree.get_children():
            self.playlists_tree.delete(item)
        
        # Add playlists to the treeview
        for playlist in playlists:
            self.playlists_tree.insert("", "end", values=(
                playlist.name,
                "✏️",  # Edit icon
                "❌"   # Delete icon
            ))
            
    def show_add_form(self):
        """Muestra el formulario para agregar playlist (modo agregar)"""
        self._edit_mode = False
        self.form_fields_frame.pack(fill="x", expand=True)
        self.form_actions_frame.pack(fill="x", pady=(5, 2))
        self.form_buttons_inner_frame.pack(side="left", padx=10)
        self.back_button_alone.pack_forget()  # Oculta el botón solo
        self.url_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.save_button.config(text="Guardar", command=self.save_new_playlist)

    def hide_add_form(self):
        """Oculta los campos y botones guardar/cancelar, muestra solo el botón volver"""
        self.form_fields_frame.pack_forget()
        self.form_actions_frame.pack_forget()
        self.back_button_alone.pack(side="left", padx=2)

    def show_edit_form(self, playlist: Playlist):
        """Muestra el formulario para editar playlist (modo edición)"""
        self._edit_mode = True
        self.form_fields_frame.pack(fill="x", expand=True)
        self.form_actions_frame.pack(fill="x", pady=(5, 2))
        self.form_buttons_inner_frame.pack(side="left", padx=10)
        self.back_button_alone.pack_forget()  # Oculta el botón solo
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, playlist.url)
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, playlist.playlist_id)
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, playlist.name)
        self.save_button.config(text="Guardar cambios", command=self.update_playlist)
        self._editing_item_id = playlist.playlist_id

    def add_playlist(self):
        """Handler para el botón de agregar playlist"""
        self.show_add_form()

    def save_new_playlist(self):
        
        playlist_id = self.id_entry.get()
        name = self.name_entry.get()
        print(f"Guardar playlist: id={playlist_id}, nombre={name}")
        self.trigger_event("save_new_playlist", playlist_id, name)
        self.hide_add_form()
        # Aquí se puede agregar lógica para notificar al controlador

    def edit_playlist(self, item_id):
        """Handler for edit playlist action"""
        # Obtener datos del item seleccionado
        values = self.playlists_tree.item(item_id)['values']
        playlist = Playlists.get_playlist_by_name(values[0])
        
        self.show_edit_form(playlist)

    def update_playlist(self):
        playlist_to_edit = Playlists.get_playlist(self._editing_item_id)
        if playlist_to_edit is None:
            print(f"Playlist with ID {self._editing_item_id} not found.")
            return
        playlist_id = self.id_entry.get()
        name = self.name_entry.get()
        print(f"Actualizar playlist: id={playlist_id}, nombre={name}")
        self.trigger_event("update_playlist", playlist_to_edit, playlist_id, name)
        self.hide_add_form()

    def save_edited_playlist(self):
        """Guardar cambios de la playlist editada"""
        playlist_id = self.edit_id_entry.get()
        name = self.edit_name_entry.get()
        print(f"Guardar edición playlist: id={playlist_id}, nombre={name}")
        self.trigger_event("save_edited_playlist", playlist_id, name)
        self.hide_edit_form()

    def delete_playlist(self, item_id):
        """Handler for delete playlist action"""
        # Mostrar confirmación de borrado
              
        values = self.playlists_tree.item(item_id)['values']
        playlist = Playlists.get_playlist_by_name(values[0])  
        self._delete_item_id = playlist.playlist_id
        
        self.form_fields_frame.pack_forget()
        self.form_actions_frame.pack_forget()
        self.delete_confirm_frame.pack(fill="x", pady=10)

    def hide_delete_confirm(self):
        """Oculta el contenedor de confirmación de borrado y muestra el botón volver"""
        self.delete_confirm_frame.pack_forget()
        

    def confirm_delete_playlist(self):
        """Confirma el borrado de la playlist"""
        
        self.trigger_event("delete_playlist", self._delete_item_id)
        self.delete_confirm_frame.pack_forget()

    def on_item_double_click(self, event):
        """Handle double click on tree item"""
        region = self.playlists_tree.identify("region", event.x, event.y)
        if (region == "cell"):
            column = self.playlists_tree.identify_column(event.x)
            item = self.playlists_tree.identify_row(event.y)
            
            # Get column number (column returns like #1, #2, etc.)
            col_num = int(column.replace('#', ''))
            
            if col_num == 2:  # Edit column
                self.edit_playlist(item)
            elif col_num == 3:  # Delete column
                self.delete_playlist(item)

    def extract_data_from_url(self):
        """Handler para el botón 'Extraer datos desde url'"""
        url = self.url_entry.get()
        self.trigger_event("extract_data_from_url", url)

    def on_url_data_extracted(self, playlist_id, name):
        """Recibe datos extraídos desde el controller y los muestra en el formulario"""
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, playlist_id)
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)

