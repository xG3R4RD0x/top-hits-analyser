import tkinter as tk
from tkinter import ttk


class BaseView(ttk.Frame):
    """Base class for all views/frames of the application."""

    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self._event_handlers = {}

        # Common configuration for all frames
        self.configure(style="TFrame", padding="10")

        # If controller is provided, connect view and controller
        if self.controller:
            self.controller.set_view(self)

        # Each subclass must implement its own interface
        self.setup_ui()

    def setup_ui(self):
        """Method that each subclass must implement to set up its UI."""
        raise NotImplementedError("Subclasses must implement this method")

    def register_event_handler(self, event_name, handler):
        """Register a handler for a specific event."""
        self._event_handlers[event_name] = handler

    def trigger_event(self, event_name, *args, **kwargs):
        """Trigger an event with the provided arguments."""
        if event_name in self._event_handlers:
            return self._event_handlers[event_name](*args, **kwargs)
        else:
            print(f"Warning: No handler registered for event '{event_name}'")
