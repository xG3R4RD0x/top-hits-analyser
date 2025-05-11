import tkinter as tk
from tkinter import ttk

from app.view.base_view import BaseView


class ManagePlaylistsView(BaseView):
    """View to display playlists"""

    def setup_ui(self):
        # View title
        self.view_label = ttk.Label(
            self, text="Manage Playlists", font=("Helvetica", 14)
        )
        self.view_label.pack(pady=10)

        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Action buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="x", pady=10)
        
        self.back_button = ttk.Button(
            self.buttons_frame,
            text="Back to Main Menu",
            command=self.go_to_main_menu,
        )
        self.back_button.pack(side="left", padx=10)
        
        # Playlists management section
        self.playlists_frame = ttk.LabelFrame(self.main_frame, text="Current Playlists")
        self.playlists_frame.pack(fill="both", expand=True, pady=10)
        
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

       
        # Log frame
        self.log_frame = ttk.Frame(self.main_frame)
        self.log_frame.pack(fill="both", expand=True, pady=10)
        
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
            
    def add_playlist(self):
        """Handler for add playlist button"""
        # This will be connected to controller later
        print("Add playlist clicked")
        
    def edit_playlist(self, item_id):
        """Handler for edit playlist action"""
        # This will be connected to controller later
        playlist_name = self.playlists_tree.item(item_id)['values'][0]
        print(f"Edit playlist: {playlist_name}")
        
    def delete_playlist(self, item_id):
        """Handler for delete playlist action"""
        # This will be connected to controller later
        playlist_name = self.playlists_tree.item(item_id)['values'][0]
        print(f"Delete playlist: {playlist_name}")
        
    def on_item_double_click(self, event):
        """Handle double click on tree item"""
        region = self.playlists_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.playlists_tree.identify_column(event.x)
            item = self.playlists_tree.identify_row(event.y)
            
            # Get column number (column returns like #1, #2, etc.)
            col_num = int(column.replace('#', ''))
            
            if col_num == 2:  # Edit column
                self.edit_playlist(item)
            elif col_num == 3:  # Delete column
                self.delete_playlist(item)