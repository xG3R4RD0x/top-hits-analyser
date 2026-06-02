import tkinter as tk
from tkinter import ttk
import sys
import os

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from app.view.base_view import BaseView
    from app.controller.update_db_controller import UpdateDBController
    class MockMainController:
        def navigate_to(self, view_name):
            print(f"MockMainController: Navigating to {view_name}")
else:
    from app.view.base_view import BaseView


class PlaylistSection(ttk.Frame):
    """A collapsible section for a playlist with lazy-loaded song checkboxes"""

    def __init__(self, parent, playlist_id, playlist_name, fetch_callback=None):
        super().__init__(parent, style="TFrame")
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
        self.fetch_callback = fetch_callback
        self._loaded = False
        self.expanded = False
        self.song_vars = {}

        self.select_all_var = tk.BooleanVar(value=False)

        def on_select_all(*args):
            val = self.select_all_var.get()
            for v in self.song_vars.values():
                v.set(val)
        self.select_all_var.trace("w", on_select_all)

        # Header
        self.header_frame = ttk.Frame(self, style="TFrame")
        self.header_frame.pack(fill="x", padx=5, pady=1)

        self.collapse_btn = ttk.Button(
            self.header_frame, text="\u25B6", width=2,
            command=self.toggle_collapse,
        )
        self.collapse_btn.pack(side="left", padx=(0, 2))

        self.name_label = ttk.Label(
            self.header_frame, text=playlist_name,
            font=("Helvetica", 10, "bold"),
        )
        self.name_label.pack(side="left", padx=2)

        self.select_all_cb = ttk.Checkbutton(
            self.header_frame, text="All",
            variable=self.select_all_var,
        )
        self.select_all_cb.pack(side="right", padx=5)

        self.songs_frame = ttk.Frame(self, style="TFrame")

    def toggle_collapse(self):
        self.expanded = not self.expanded
        if self.expanded:
            if not self._loaded:
                self._load_songs()
            self.songs_frame.pack(fill="x", padx=(15, 0))
            self.collapse_btn.config(text="\u25BC")
        else:
            self.songs_frame.pack_forget()
            self.collapse_btn.config(text="\u25B6")

    def _load_songs(self):
        if not self.fetch_callback:
            return
        songs = self.fetch_callback(self.playlist_id)
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

                ttk.Checkbutton(
                    row, text=f"{song.artist} - {song.name}",
                    variable=var,
                ).pack(side="left", padx=5)

            if self.select_all_var.get():
                for v in self.song_vars.values():
                    v.set(True)

        self._loaded = True


class UpdateDBView(BaseView):
    """View with collapsible playlist sections, lazy song loading, and global select"""

    _mousewheel_bound = False

    def setup_ui(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

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

        # Mouse wheel scrolling - bind_all captures events over child widgets too
        if not UpdateDBView._mousewheel_bound:
            self.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
            UpdateDBView._mousewheel_bound = True

        self.canvas.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        self.scrollbar.pack(side="right", fill="y", pady=5)

        # Global Select All checkbox
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

        # Action buttons
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(fill="x", pady=5)

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

        # Collapsible Log section
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

    def load_playlists(self, playlists_data):
        """Load playlists (names only, songs lazy-loaded on expand)"""
        # Keep global Select All if it exists
        for widget in self.playlist_inner.winfo_children():
            widget.destroy()
        self.playlist_sections.clear()

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

        # Build sections with lazy load callback
        for playlist, _ in playlists_data:
            section = PlaylistSection(
                self.playlist_inner,
                playlist.playlist_id,
                playlist.name,
                fetch_callback=lambda pid: self.trigger_event("fetch_playlist_songs", pid),
            )
            section.pack(fill="x", padx=5, pady=2)
            self.playlist_sections[playlist.playlist_id] = section

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
