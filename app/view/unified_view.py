import tkinter as tk
from tkinter import ttk
import sys
import os

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from app.view.base_view import BaseView
    from app.controller.unified_controller import UnifiedController
    class MockMainController:
        def navigate_to(self, view_name):
            print(f"MockMainController: Navigating to {view_name}")
else:
    from app.view.base_view import BaseView


class PlaylistSection(ttk.Frame):
    """A collapsible section for a playlist with pre-loaded songs"""

    def __init__(self, parent, playlist_id, playlist_name):
        super().__init__(parent, style="TFrame")
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
        self.songs = []
        self.song_vars = {}
        self.expanded = False

        self.select_all_var = tk.BooleanVar(value=False)

        def on_select_all(*args):
            val = self.select_all_var.get()
            for v in self.song_vars.values():
                v.set(val)
        self.select_all_var.trace("w", on_select_all)

        self.grid_columnconfigure(1, weight=1)

        self.collapse_btn = ttk.Button(
            self, text="\u25B6", width=2,
            command=self.toggle_collapse,
        )
        self.collapse_btn.grid(row=0, column=0, padx=(5, 2), pady=1, sticky="w")

        self.name_label = ttk.Label(
            self, text="",
            font=("Helvetica", 10, "bold"),
        )
        self.name_label.grid(row=0, column=1, padx=2, pady=1, sticky="w")
        self._update_name_label()

        self.select_all_cb = ttk.Checkbutton(
            self, text="All",
            variable=self.select_all_var,
        )
        self.select_all_cb.grid(row=0, column=2, padx=5, pady=1, sticky="e")

        self.songs_frame = ttk.Frame(self, style="TFrame")

    def _update_name_label(self):
        self.name_label.config(text=f"{self.playlist_name} ({len(self.songs)})")

    def set_songs(self, songs):
        self.songs = songs
        self._update_name_label()
        for widget in self.songs_frame.winfo_children():
            widget.destroy()
        self.song_vars.clear()

        if not songs:
            ttk.Label(self.songs_frame, text="  No songs found",
                      font=("Helvetica", 9)).pack(anchor="w", padx=10)
        else:
            for song in songs:
                var = tk.BooleanVar(value=False)
                self.song_vars[song.id] = var

                row = ttk.Frame(self.songs_frame, style="TFrame")
                row.pack(fill="x", pady=1)

                album_text = song.album if song.album else "-"
                display_text = f"{song.artist} - {song.name} ({album_text})"

                ttk.Checkbutton(
                    row, text=display_text, variable=var,
                ).pack(side="left", padx=5)

        if self.select_all_var.get():
            for v in self.song_vars.values():
                v.set(True)

    def toggle_collapse(self):
        self.expanded = not self.expanded
        if self.expanded:
            self.songs_frame.grid(row=1, column=0, columnspan=3,
                                  sticky="ew", padx=(15, 0))
            self.collapse_btn.config(text="\u25BC")
        else:
            self.songs_frame.grid_remove()
            self.collapse_btn.config(text="\u25B6")

    def expand(self):
        if not self.expanded:
            self.toggle_collapse()

    def collapse(self):
        if self.expanded:
            self.toggle_collapse()


class UnifiedView(BaseView):
    """Combined view: filterable playlist sections with song selection, actions, and log"""

    _mousewheel_bound = False

    def setup_ui(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Filter bar
        self.filter_frame = ttk.Frame(self.main_frame)
        self.filter_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(self.filter_frame, text="Search:").pack(side="left", padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.apply_filters())
        self.search_entry = ttk.Entry(self.filter_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side="left", padx=(0, 10))

        ttk.Label(self.filter_frame, text="Playlist:").pack(side="left", padx=(0, 5))
        self.playlist_var = tk.StringVar(value="All")
        self.playlist_combo = ttk.Combobox(
            self.filter_frame, textvariable=self.playlist_var, width=15, state="readonly"
        )
        self.playlist_combo.pack(side="left", padx=(0, 10))
        self.playlist_combo.bind("<<ComboboxSelected>>", lambda *args: self.apply_filters())

        ttk.Label(self.filter_frame, text="Artist:").pack(side="left", padx=(0, 5))
        self.artist_var = tk.StringVar(value="All")
        self.artist_combo = ttk.Combobox(
            self.filter_frame, textvariable=self.artist_var, width=15, state="readonly"
        )
        self.artist_combo.pack(side="left", padx=(0, 10))
        self.artist_combo.bind("<<ComboboxSelected>>", lambda *args: self.apply_filters())

        self.reset_button = ttk.Button(
            self.filter_frame, text="Reset Filters",
            command=self.reset_filters,
        )
        self.reset_button.pack(side="left", padx=5)

        # Action buttons
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(fill="x", pady=(0, 10))

        self.update_button = ttk.Button(
            self.buttons_frame, text="Update Selected",
            command=self.start_operation)
        self.update_button.pack(side="left", padx=5)

        self.fetch_button = ttk.Button(
            self.buttons_frame, text="Fetch URLs",
            command=self.fetch_songs_urls)
        self.fetch_button.pack(side="left", padx=5)

        self.download_button = ttk.Button(
            self.buttons_frame, text="Download",
            command=self.download_songs)
        self.download_button.pack(side="left", padx=5)

        self.cancel_button = ttk.Button(
            self.buttons_frame, text="Cancel",
            command=self.cancel_operation)
        self.cancel_button.pack(side="right", padx=5)

        # Progress bar
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="Progress")
        self.progress_frame.pack(fill="x", pady=(0, 10))

        self.progress_label = ttk.Label(self.progress_frame, text="Status:")
        self.progress_label.pack(side="left", padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(
            self.progress_frame, length=400, mode="determinate", orient="horizontal"
        )
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.progress_percentage = ttk.Label(
            self.progress_frame, text="0%", font=("Helvetica", 10, "bold"))
        self.progress_percentage.pack(side="left", padx=5, pady=5)

        # Scrollable playlist area
        self.playlist_container = ttk.LabelFrame(self.main_frame, text="Playlists")
        self.playlist_container.pack(fill="both", expand=True, pady=(0, 10))

        self.canvas = tk.Canvas(self.playlist_container, bg="#f0f0f0", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(
            self.playlist_container, orient="vertical", command=self.canvas.yview
        )
        self.playlist_inner = ttk.Frame(self.canvas, style="TFrame")

        self.playlist_inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.playlist_inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        if not UnifiedView._mousewheel_bound:
            self.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
            UnifiedView._mousewheel_bound = True

        self.canvas.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        self.scrollbar.pack(side="right", fill="y", pady=5)

        # Global Select All
        self.global_select_all_var = tk.BooleanVar(value=False)
        self.global_select_frame = ttk.Frame(self.playlist_inner, style="TFrame")
        self.global_select_frame.pack(fill="x", padx=5, pady=2)

        ttk.Checkbutton(
            self.global_select_frame,
            text="Select All Playlists",
            variable=self.global_select_all_var,
        ).pack(side="left", padx=5)

        def on_global_select_all(*args):
            val = self.global_select_all_var.get()
            for section in self.playlist_sections.values():
                section.select_all_var.set(val)
        self.global_select_all_var.trace("w", on_global_select_all)

        self.playlist_sections = {}
        self.playlist_sections_in_order = []
        self.all_songs = []
        self.all_playlists_data = []

        # Log section
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Log")
        self.log_frame.pack(fill="x", pady=(5, 0))

        self.log_toggle_btn = tk.Button(
            self.log_frame, text="\u25B6 Show Logs",
            bd=0, bg="#f0f0f0", activebackground="#e0e0e0",
            cursor="hand2", command=self.toggle_log,
        )
        self.log_toggle_btn.pack(anchor="w", padx=5, pady=2)

        self.log_content = ttk.Frame(self.log_frame)

        self.log_text = tk.Text(
            self.log_content, wrap=tk.WORD, height=6,
            font=("Courier", 9))
        self.log_scrollbar = ttk.Scrollbar(self.log_content, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scrollbar.set, state="disabled")

        self.log_text.pack(side="left", fill="both", expand=True)
        self.log_scrollbar.pack(side="right", fill="y")

        self.log_expanded = False

        # State
        self.is_operation_running = False
        self.cancelled = False

    def _on_mousewheel(self, event):
        w = self.winfo_containing(event.x_root, event.y_root)
        while w:
            if w == self.playlist_container:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return "break"
            w = w.master

    def toggle_log(self):
        self.log_expanded = not self.log_expanded
        if self.log_expanded:
            self.log_content.pack(fill="x", padx=5, pady=(0, 5))
            self.log_toggle_btn.config(text="\u25BC Hide Logs")
        else:
            self.log_content.pack_forget()
            self.log_toggle_btn.config(text="\u25B6 Show Logs")

    def load_data(self, playlists_data):
        """Load data: playlists_data is [(Playlist, [Song]), ...]"""
        for widget in self.playlist_inner.winfo_children():
            widget.destroy()
        self.playlist_sections.clear()
        self.all_playlists_data = playlists_data
        self.all_songs = [song for _, songs in playlists_data for song in songs]

        # Rebuild global Select All
        self.global_select_all_var = tk.BooleanVar(value=False)
        self.global_select_frame = ttk.Frame(self.playlist_inner, style="TFrame")
        self.global_select_frame.pack(fill="x", padx=5, pady=2)

        ttk.Checkbutton(
            self.global_select_frame,
            text="Select All Playlists",
            variable=self.global_select_all_var,
        ).pack(side="left", padx=5)

        def on_global_select_all(*args):
            val = self.global_select_all_var.get()
            for section in self.playlist_sections.values():
                section.select_all_var.set(val)
        self.global_select_all_var.trace("w", on_global_select_all)

        # Build sections with pre-loaded songs
        self.playlist_sections_in_order.clear()
        for playlist, songs in playlists_data:
            section = PlaylistSection(
                self.playlist_inner,
                playlist.playlist_id,
                playlist.name,
            )
            section.set_songs(songs)
            section.pack(fill="x", padx=5, pady=2)
            self.playlist_sections[playlist.playlist_id] = section
            self.playlist_sections_in_order.append(playlist.playlist_id)

        # Populate filter dropdowns
        self._update_filter_dropdowns()

        # Apply current filter if active
        if self._has_active_filter():
            self.apply_filters()

    def _update_filter_dropdowns(self):
        playlists = ["All"] + sorted(set(
            pl.name for pl, _ in self.all_playlists_data
        ))
        current_pl = self.playlist_var.get()
        self.playlist_combo["values"] = playlists
        if current_pl in playlists:
            self.playlist_var.set(current_pl)
        else:
            self.playlist_var.set("All")

        artists = ["All"] + sorted(set(
            song.artist for song in self.all_songs
        ))
        current_ar = self.artist_var.get()
        self.artist_combo["values"] = artists
        if current_ar in artists:
            self.artist_var.set(current_ar)
        else:
            self.artist_var.set("All")

    def _has_active_filter(self):
        return bool(self.search_var.get()) or \
               self.playlist_var.get() != "All" or \
               self.artist_var.get() != "All"

    def apply_filters(self):
        search_text = self.search_var.get().lower()
        playlist_filter = self.playlist_var.get()
        artist_filter = self.artist_var.get()

        has_filter = bool(search_text) or playlist_filter != "All" or artist_filter != "All"

        # Group matching songs by playlist_id
        visible = {}
        for pl, songs in self.all_playlists_data:
            matching = [
                s for s in songs
                if (not search_text or search_text in s.name.lower() or search_text in s.artist.lower())
                and (playlist_filter == "All" or s.playlist_name == playlist_filter)
                and (artist_filter == "All" or s.artist == artist_filter)
            ]
            if matching or not has_filter:
                visible[pl.playlist_id] = matching

        # Forget all sections, then repack visible ones in order
        for pid in self.playlist_sections_in_order:
            self.playlist_sections[pid].pack_forget()

        for pid in self.playlist_sections_in_order:
            section = self.playlist_sections[pid]
            if pid in visible:
                section.set_songs(visible[pid])
                section.pack(fill="x", padx=5, pady=2)
                if has_filter:
                    section.expand()
                else:
                    section.collapse()

    def reset_filters(self):
        self.search_var.set("")
        self.playlist_var.set("All")
        self.artist_var.set("All")
        self.apply_filters()

    def get_selected_playlist_ids(self):
        ids = []
        for pid, section in self.playlist_sections.items():
            if any(v.get() for v in section.song_vars.values()):
                ids.append(pid)
        return ids

    def get_selected_song_ids(self):
        ids = []
        for section in self.playlist_sections.values():
            for sid, var in section.song_vars.items():
                if var.get():
                    ids.append(sid)
        return ids

    def update_progress(self, value, text=None):
        self.progress_bar["value"] = value
        if text is None:
            self.progress_percentage["text"] = f"{int(value)}%"
        else:
            self.progress_percentage["text"] = text
        self.update_idletasks()

    def add_log_message(self, message):
        if not self.log_expanded:
            self.toggle_log()
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")
        self.update_idletasks()

    def start_operation(self):
        ids = self.get_selected_playlist_ids()
        if not ids:
            self.add_log_message("No playlists selected")
            return
        self.is_operation_running = True
        self.cancelled = False
        self.cancel_button["state"] = "normal"
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")
        self.update_progress(0)
        self.add_log_message("Starting database update...")
        self.trigger_event("start_update", ids)

    def fetch_songs_urls(self):
        ids = self.get_selected_song_ids()
        if not ids:
            self.add_log_message("No songs selected")
            return
        self.is_operation_running = True
        self.cancelled = False
        self.cancel_button["state"] = "normal"
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")
        self.update_progress(0)
        self.add_log_message("Starting URL fetch...")
        self.trigger_event("fetch_urls", ids)

    def download_songs(self):
        ids = self.get_selected_song_ids()
        if not ids:
            self.add_log_message("No songs selected")
            return
        self.is_operation_running = True
        self.cancelled = False
        self.cancel_button["state"] = "normal"
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")
        self.update_progress(0)
        self.add_log_message("Starting download...")
        self.trigger_event("download_songs", ids)

    def complete_operation(self, success=True):
        self.is_operation_running = False
        self.cancel_button["state"] = "disabled"
        if success:
            self.update_progress(100, "Done")
            self.add_log_message("Operation completed successfully.")
        else:
            if self.cancelled:
                self.add_log_message("Operation cancelled by user.")
            else:
                self.add_log_message("Operation failed. Check details above.")

    def cancel_operation(self):
        self.trigger_event("cancel_update_operation")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x650")
    mock_ctrl = MockMainController()
    from app.model.playlist import Playlist
    from app.model.song import Song

    view = UnifiedView(root, controller=mock_ctrl)

    pl1 = Playlist("pl1", "Rock Hits")
    pl2 = Playlist("pl2", "Pop Favorites")

    songs1 = [
        Song(id=1, playlist_name="Rock Hits", playlist_id="pl1", name="Bohemian Rhapsody",
             artist="Queen", album="A Night at the Opera"),
        Song(id=2, playlist_name="Rock Hits", playlist_id="pl1", name="Stairway to Heaven",
             artist="Led Zeppelin", album="Led Zeppelin IV"),
    ]
    songs2 = [
        Song(id=3, playlist_name="Pop Favorites", playlist_id="pl2", name="Blinding Lights",
             artist="The Weeknd", album="After Hours"),
        Song(id=4, playlist_name="Pop Favorites", playlist_id="pl2", name="Levitating",
             artist="Dua Lipa", album=None),
    ]

    view.load_data([(pl1, songs1), (pl2, songs2)])
    view.pack(fill="both", expand=True)
    root.mainloop()
