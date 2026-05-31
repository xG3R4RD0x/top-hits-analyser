import tkinter as tk
from tkinter import ttk, messagebox

from app.view.base_view import BaseView
from app.model.playlists import Playlists
from app.model.playlist import Playlist


class ManagePlaylistsView(BaseView):
    """View to manage playlists with icons and proper form handling"""

    def setup_ui(self):
        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # State: only one form can be open at a time
        self._current_form_type = None  # "add", "edit", or "delete"
        self._editing_playlist_id = None
        self._deleting_playlist_id = None

        # Playlists section
        self.playlists_section = ttk.LabelFrame(self.main_frame, text="Current Playlists")
        self.playlists_section.pack(fill="both", expand=True, pady=(0, 10))

        # Toolbar with add button
        self.toolbar_frame = ttk.Frame(self.playlists_section)
        self.toolbar_frame.pack(fill="x", padx=5, pady=5)

        self.add_button = ttk.Button(
            self.toolbar_frame, 
            text="+ Add Playlist", 
            command=self.add_playlist
        )
        self.add_button.pack(side="left", padx=5)

        # Playlists treeview with icons
        self.playlists_tree = ttk.Treeview(
            self.playlists_section,
            columns=("name", "edit", "delete"),
            show="headings",
            selectmode="browse",
            height=12
        )
        
        # Define columns
        self.playlists_tree.heading("name", text="Playlist Name")
        self.playlists_tree.heading("edit", text="Edit")
        self.playlists_tree.heading("delete", text="Delete")
        
        # Column widths
        self.playlists_tree.column("name", width=250, anchor="w")
        self.playlists_tree.column("edit", width=50, anchor="center")
        self.playlists_tree.column("delete", width=50, anchor="center")
          
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.playlists_section, 
            orient="vertical", 
            command=self.playlists_tree.yview
        )
        self.playlists_tree.configure(yscrollcommand=scrollbar.set)
        
        # Place treeview and scrollbar
        self.playlists_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=5)
        
        # Bind single-click to handle actions
        self.playlists_tree.bind("<Button-1>", self.on_item_click)

        # --- Form Section: Single form for Add/Edit (initially hidden) ---
        self.form_section = ttk.LabelFrame(self.main_frame, text="Add/Edit Playlist")
        # Don't pack yet - only show when needed
        
        # Form fields grid
        self.form_fields_frame = ttk.Frame(self.form_section)
        self.form_fields_frame.pack(fill="x", expand=True, padx=5, pady=5)
        self.form_fields_frame.grid_columnconfigure(1, weight=1)

        # URL field with extract button
        ttk.Label(self.form_fields_frame, text="URL:").grid(row=0, column=0, sticky="w", padx=2, pady=5)
        self.url_entry = ttk.Entry(self.form_fields_frame)
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=2, pady=5)
        self.extract_button = ttk.Button(
            self.form_fields_frame,
            text="Extract from URL",
            command=self.extract_data_from_url
        )
        self.extract_button.grid(row=0, column=2, sticky="w", padx=2, pady=5)

        # ID field
        ttk.Label(self.form_fields_frame, text="Playlist ID:").grid(row=1, column=0, sticky="w", padx=2, pady=5)
        self.id_entry = ttk.Entry(self.form_fields_frame)
        self.id_entry.grid(row=1, column=1, sticky="ew", padx=2, pady=5)

        # Name field
        ttk.Label(self.form_fields_frame, text="Name:").grid(row=2, column=0, sticky="w", padx=2, pady=5)
        self.name_entry = ttk.Entry(self.form_fields_frame)
        self.name_entry.grid(row=2, column=1, sticky="ew", padx=2, pady=5)

        # Form action buttons
        self.form_actions_frame = ttk.Frame(self.form_section)
        self.form_actions_frame.pack(fill="x", padx=5, pady=(0, 5))

        self.save_button = ttk.Button(
            self.form_actions_frame, 
            text="Save", 
            command=self.save_playlist
        )
        self.save_button.pack(side="left", padx=5)

        self.cancel_button = ttk.Button(
            self.form_actions_frame, 
            text="Cancel", 
            command=self.cancel_form
        )
        self.cancel_button.pack(side="left", padx=5)

        # Delete confirmation section (only for delete operations)
        self.delete_confirm_frame = ttk.Frame(self.form_section)
        self.delete_confirm_label = ttk.Label(
            self.delete_confirm_frame,
            text="Are you sure you want to delete this playlist?",
            foreground="red",
            font=("Helvetica", 10, "bold")
        )
        self.delete_confirm_label.pack(side="top", pady=5, padx=10)
        
        delete_buttons = ttk.Frame(self.delete_confirm_frame)
        delete_buttons.pack(side="top", padx=10)
        
        self.delete_yes_button = ttk.Button(
            delete_buttons,
            text="Yes, Delete",
            command=self.confirm_delete_playlist
        )
        self.delete_yes_button.pack(side="left", padx=5)
        
        self.delete_cancel_button = ttk.Button(
            delete_buttons,
            text="Cancel",
            command=self.cancel_form
        )
        self.delete_cancel_button.pack(side="left", padx=5)

    def load_playlists(self, playlists):
        """Load playlists into the treeview with emoji icons"""
        # Clear existing items
        for item in self.playlists_tree.get_children():
            self.playlists_tree.delete(item)
        
        # Add playlists with emoji icons
        for i, playlist in enumerate(playlists):
            self.playlists_tree.insert("", "end", iid=f"pl_{i}", values=(
                playlist.name,
                "✏️",   # Edit icon
                "❌"   # Delete icon (red X)
            ))

    def on_item_click(self, event):
        """Handle single-click on tree item"""
        region = self.playlists_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.playlists_tree.identify_column(event.x)
            item = self.playlists_tree.identify_row(event.y)
            col_num = int(column.replace('#', ''))
            
            # Close any open form first
            self.close_form()
            
            # Get the playlist
            values = self.playlists_tree.item(item)['values']
            playlist_name = values[0]
            playlist = Playlists.get_playlist_by_name(playlist_name)
            
            if col_num == 2:  # Edit column
                self.start_edit(playlist)
            elif col_num == 3:  # Delete column
                self.start_delete(playlist)

    def add_playlist(self):
        """Start adding a new playlist"""
        self.close_form()
        self._current_form_type = "add"
        self._editing_playlist_id = None
        
        # Clear form fields
        self.clear_form()
        self.save_button.config(text="Add Playlist")
        
        # Show form section with edit/add fields
        self.form_section.pack(fill="x", padx=5, pady=(10, 5))
        self.form_fields_frame.pack(fill="x", expand=True, padx=5, pady=5)
        self.form_actions_frame.pack(fill="x", padx=5, pady=(0, 5))
        self.delete_confirm_frame.pack_forget()

    def start_edit(self, playlist: Playlist):
        """Start editing a playlist"""
        self._current_form_type = "edit"
        self._editing_playlist_id = playlist.playlist_id
        
        # Populate form with playlist data
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, playlist.url or "")
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, playlist.playlist_id or "")
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, playlist.name or "")
        
        self.save_button.config(text="Save Changes")
        
        # Show form section with edit fields
        self.form_section.pack(fill="x", padx=5, pady=(10, 5))
        self.form_fields_frame.pack(fill="x", expand=True, padx=5, pady=5)
        self.form_actions_frame.pack(fill="x", padx=5, pady=(0, 5))
        self.delete_confirm_frame.pack_forget()

    def start_delete(self, playlist: Playlist):
        """Start deleting a playlist"""
        self._current_form_type = "delete"
        self._deleting_playlist_id = playlist.playlist_id
        
        # Show form section with delete confirmation
        self.form_section.pack(fill="x", padx=5, pady=(10, 5))
        self.form_fields_frame.pack_forget()
        self.form_actions_frame.pack_forget()
        self.delete_confirm_frame.pack(fill="x", padx=5, pady=5)

    def save_playlist(self):
        """Save new or updated playlist"""
        playlist_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        
        if not playlist_id or not name:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if self._current_form_type == "edit":
            playlist = Playlists.get_playlist(self._editing_playlist_id)
            self.trigger_event("update_playlist", playlist, playlist_id, name)
        else:
            self.trigger_event("save_new_playlist", playlist_id, name)
        
        self.close_form()

    def confirm_delete_playlist(self):
        """Confirm deletion"""
        self.trigger_event("delete_playlist", self._deleting_playlist_id)
        self.close_form()

    def cancel_form(self):
        """Cancel any operation"""
        self.close_form()

    def close_form(self):
        """Hide the form section completely"""
        self.form_section.pack_forget()
        self._current_form_type = None
        self._editing_playlist_id = None
        self._deleting_playlist_id = None

    def clear_form(self):
        """Clear all form fields"""
        self.url_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)

    def extract_data_from_url(self):
        """Extract playlist data from URL"""
        url = self.url_entry.get().strip()
        if url:
            self.trigger_event("extract_data_from_url", url)

    def on_url_data_extracted(self, playlist_id, name):
        """Receive extracted data and populate form"""
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, playlist_id)
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
