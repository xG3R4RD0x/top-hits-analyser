import tkinter as tk
from tkinter import ttk
import sys
import os

# Special adjustment for imports when run directly
if __name__ == "__main__":
    # Get the absolute path to the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # Add the root directory to Python's path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Direct imports for independent execution
    from app.view.base_view import BaseView
    from app.controller.update_db_controller import UpdateDBController

    # Create a mock controller for testing
    class MockMainController:
        def navigate_to(self, view_name):
            print(f"MockMainController: Navigating to {view_name}")

else:
    # Normal imports when imported as a module
    from app.view.base_view import BaseView


class UpdateDBView(BaseView):
    """View to display database update progress"""

    def setup_ui(self):
        # View title
        self.view_label = ttk.Label(
            self, text="Database Update", font=("Helvetica", 14)
        )
        self.view_label.pack(pady=10)

        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Progress bar frame
        self.progress_frame = ttk.Frame(self.main_frame)
        self.progress_frame.pack(fill="x", pady=10)

        self.progress_label = ttk.Label(self.progress_frame, text="Progress:")
        self.progress_label.pack(side="left", padx=5)

        self.progress_bar = ttk.Progressbar(
            self.progress_frame, length=500, mode="determinate", orient="horizontal"
        )
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=5)

        self.progress_percentage = ttk.Label(self.progress_frame, text="0%")
        self.progress_percentage.pack(side="left", padx=5)

        # Log frame
        self.log_frame = ttk.Frame(self.main_frame)
        self.log_frame.pack(fill="both", expand=True, pady=10)

        self.log_label = ttk.Label(self.log_frame, text="Operations Log:")
        self.log_label.pack(anchor="w")

        # Create a Text widget with scrollbar for the log
        self.log_text_frame = ttk.Frame(self.log_frame)
        self.log_text_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(self.log_text_frame, wrap=tk.WORD, height=15)
        self.log_text.pack(side="left", fill="both", expand=True)

        self.log_scrollbar = ttk.Scrollbar(
            self.log_text_frame, command=self.log_text.yview
        )
        self.log_scrollbar.pack(side="right", fill="y")

        self.log_text.config(yscrollcommand=self.log_scrollbar.set)
        self.log_text.configure(
            state="disabled"
        )  # Initially disabled to prevent editing

        # Action buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="x", pady=10)

        self.back_button = ttk.Button(
            self.buttons_frame,
            text="Back to Main Menu",
            command=self.go_to_main_menu,
        )
        self.back_button.pack(side="left", padx=10)

        self.start_update_button = ttk.Button(
            self.buttons_frame,
            text="Start Update",
            command=self.start_operation,
        )
        self.start_update_button.pack(side="left", padx=10)

        self.fetch_songs_button = ttk.Button(
            self.buttons_frame,
            text="Fetch Songs URLs",
            command=self.fetch_songs_urls,
        )
        self.fetch_songs_button.pack(side="left", padx=10)

        self.fetch_songs_button = ttk.Button(
            self.buttons_frame,
            text="Download Songs",
            command=self.download_songs,
        )
        self.fetch_songs_button.pack(side="left", padx=10)

        self.cancel_button = ttk.Button(
            self.buttons_frame, text="Cancel Operation", command=self.cancel_operation
        )
        self.cancel_button.pack(side="right", padx=10)

        # Initial state
        self.is_operation_running = False
        self.cancelled = False

    def go_to_main_menu(self):
        """Go back to main menu"""
        self.trigger_event("navigate_to", "main_menu")

    def update_progress(self, value, text=None):
        """
        Update progress bar and optionally the percentage text

        Args:
            value: Progress value (0-100)
            text: Optional text to display (if None, percentage is shown)
        """
        print(f"Updating progress: {value}%")
        self.progress_bar["value"] = value

        if text is None:
            self.progress_percentage["text"] = f"{int(value)}%"
        else:
            self.progress_percentage["text"] = text

        # Force UI update
        self.update_idletasks()

    def add_log_message(self, message):
        """
        Add a message to the log area

        Args:
            message: Message to add
        """
        # Enable the Text widget for editing
        self.log_text.configure(state="normal")

        # Add message with line break
        self.log_text.insert(tk.END, f"{message}\n")

        # Automatically scroll to the end of the text
        self.log_text.see(tk.END)

        # Disable again to prevent manual editing
        self.log_text.configure(state="disabled")

        # Force UI update
        self.update_idletasks()

    def download_songs(self):
        """Download songs from the database"""
        self.is_operation_running = True
        self.cancelled = False
        self.cancel_button["state"] = "normal"
        self.back_button["state"] = "disabled"

        # Clear the log
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")

        # Reset the progress bar
        self.update_progress(0)

        # Add an initial message
        self.add_log_message("Starting song download...")
        self.controller.download_songs()

    def fetch_songs_urls(self):
        """Fetch songs URLs from the database"""
        self.is_operation_running = True
        self.cancelled = False
        self.cancel_button["state"] = "normal"
        self.back_button["state"] = "disabled"

        # Clear the log
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")

        # Reset the progress bar
        self.update_progress(0)

        self.controller.fetch_songs_urls()

    def start_operation(self):
        """Start the update operation"""
        self.is_operation_running = True
        self.cancelled = False
        self.cancel_button["state"] = "normal"
        self.back_button["state"] = "disabled"

        # Clear the log
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")

        # Reset the progress bar
        self.update_progress(0)

        # Add an initial message
        self.add_log_message("Starting database update...")
        self.controller.start_update_process()

    def complete_operation(self, success=True):
        """Finish the operation"""
        self.is_operation_running = False
        self.cancel_button["state"] = "disabled"
        self.back_button["state"] = "normal"

        if success:
            self.update_progress(100, "Completed")
            self.add_log_message("Operation completed successfully.")
        else:
            if self.cancelled:
                self.add_log_message("Operation cancelled by user.")
            else:
                self.add_log_message("Operation failed. Check details above.")

    def cancel_operation(self):
        """Cancel the ongoing operation"""
        self.trigger_event("cancel_update_operation")


# Code for debugging and independent testing
if __name__ == "__main__":
    import time

    root = tk.Tk()
    root.title("Database Update - Independent Mode")
    root.geometry("700x500")

    # Configure style
    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")

    # Instantiate the mock controller and view
    main_controller = MockMainController()
    controller = UpdateDBController(main_controller)
    view = UpdateDBView(root, controller)
    view.pack(fill="both", expand=True)

    # Start button for simulation
    start_button = ttk.Button(
        root,
        text="Start Simulation",
        command=controller.start_update_process,
    )
    start_button.pack(pady=10)

    root.mainloop()
