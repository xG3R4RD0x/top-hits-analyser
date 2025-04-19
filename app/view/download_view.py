import tkinter as tk
from tkinter import ttk
import sys
import os
import time
import random

# Special adjustment for imports when run directly
if __name__ == "__main__":
    # Get the absolute path to the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # Add the root directory to Python's path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Direct imports for independent execution
    from app.view.base_view import BaseView

    # Create a mock controller for testing
    class MockController:
        def show_main_menu(self):
            print("MockController: Returning to main menu")

        def start_download(self):
            print("MockController: Starting download")

else:
    # Normal imports when imported as a module
    from app.view.base_view import BaseView


class DownloadView(BaseView):
    """View to display and manage downloads"""

    def setup_ui(self):
        # View title
        self.view_label = ttk.Label(self, text="Song Downloads", font=("Helvetica", 14))
        self.view_label.pack(pady=10)

        # Frame for download list and progress
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        # Create download list with progress bars
        self.create_download_list()

        # Action buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="x", pady=10)

        self.back_button = ttk.Button(
            self.buttons_frame,
            text="Back to Main Menu",
            command=self.go_to_main_menu,
        )
        self.back_button.pack(side="left", padx=5)

        self.start_button = ttk.Button(
            self.buttons_frame, text="Start Download", command=self.start_download
        )
        self.start_button.pack(side="right", padx=5)

        # Add sample downloads
        self.add_sample_downloads()

    def create_download_list(self):
        """Create the download list with progress bars"""
        # Create a frame with scrollbar
        self.download_frame = ttk.Frame(self.content_frame)
        self.download_frame.pack(fill="both", expand=True, pady=10)

        # Create a canvas with scrollbar for the download list
        self.canvas = tk.Canvas(self.download_frame)
        scrollbar = ttk.Scrollbar(
            self.download_frame, orient="vertical", command=self.canvas.yview
        )

        # Internal frame for download items
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack everything
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Variable to track download rows
        self.download_rows = {}

    def add_download_item(self, song_name, artist, status="Pending"):
        """Add a download item to the list"""
        row = len(self.download_rows)

        # Create frame for this item
        item_frame = ttk.Frame(self.scrollable_frame)
        item_frame.pack(fill="x", padx=5, pady=5)

        # Label with name and info
        label = ttk.Label(
            item_frame, text=f"{song_name} - {artist}", width=30, anchor="w"
        )
        label.grid(row=0, column=0, padx=5, sticky="w")

        # Progress bar
        progress = ttk.Progressbar(item_frame, length=300, mode="determinate", value=0)
        progress.grid(row=0, column=1, padx=5)

        # Status label
        status_label = ttk.Label(item_frame, text=status, width=15)
        status_label.grid(row=0, column=2, padx=5)

        # Save references
        self.download_rows[row] = {
            "frame": item_frame,
            "label": label,
            "progress": progress,
            "status": status_label,
            "song_name": song_name,
            "artist": artist,
        }

        return row

    def update_progress(self, row_id, progress_value, status_text=None):
        """Update the progress and status of a download"""
        if row_id in self.download_rows:
            self.download_rows[row_id]["progress"]["value"] = progress_value

            if status_text:
                self.download_rows[row_id]["status"]["text"] = status_text

            # Update the interface
            self.update_idletasks()

    def add_sample_downloads(self):
        """Add sample downloads for debugging"""
        sample_songs = [
            ("Gasolina", "Daddy Yankee"),
            ("Hawái", "Maluma"),
            ("Despacito", "Luis Fonsi"),
            ("Con Calma", "Daddy Yankee"),
            ("Taki Taki", "DJ Snake"),
            ("Mi Gente", "J Balvin"),
            ("Baila Conmigo", "Selena Gomez"),
            ("Dákiti", "Bad Bunny"),
            ("La Canción", "J Balvin & Bad Bunny"),
            ("Ginza", "J Balvin"),
        ]

        for song_name, artist in sample_songs:
            self.add_download_item(song_name, artist)

    def simulate_download_progress(self, row_id):
        """Simulate download progress for debugging"""
        progress = 0
        statuses = ["Downloading", "Processing", "Completed"]
        current_status = 0

        self.update_progress(row_id, progress, statuses[current_status])

        while progress < 100:
            # Simulate random progress
            progress += random.randint(1, 10)
            progress = min(progress, 100)

            # Change status sometimes
            if progress > 50 and current_status == 0:
                current_status = 1

            if progress == 100:
                current_status = 2

            # Update UI
            self.update_progress(row_id, progress, statuses[current_status])

            # Wait some time
            time.sleep(0.3)

            # Update UI
            self.update()

    def go_to_main_menu(self):
        """Go back to main menu"""
        self.trigger_event("navigate_to", "main_menu")

    def start_download(self):
        """Start song download"""
        self.trigger_event("start_download")


# Run the view independently when run directly
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Downloads - Independent Mode")
    root.geometry("800x600")

    # Configure style
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")

    # Instantiate the mock controller and view
    controller = MockController()
    view = DownloadView(root, controller)
    view.pack(fill="both", expand=True)

    # Add a test button to simulate a download for a specific song
    def test_download():
        # Get the first row ID
        if view.download_rows:
            first_row = next(iter(view.download_rows))
            view.simulate_download_progress(first_row)

    test_button = ttk.Button(root, text="Test Download", command=test_download)
    test_button.pack(pady=10)

    # Run the application
    root.mainloop()
