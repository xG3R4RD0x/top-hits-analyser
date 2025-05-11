import tkinter as tk
from tkinter import ttk


class BaseView(ttk.Frame):
    """Base class for all views/frames of the application."""
    
    # Dictionary to store singleton instances of each subclass
    _instances = {}

    def __new__(cls, parent, controller=None):
        """Override __new__ to implement the singleton pattern"""
        # Check if an instance of this specific class (not parent class) already exists
        if cls not in cls._instances:
            # Create a new instance
            instance = super(BaseView, cls).__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self, parent, controller=None):
        # Check if this instance has been initialized before
        if not hasattr(self, '_initialized'):
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
            
            # Mark as initialized so __init__ won't run again on the same instance
            self._initialized = True

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
            
    def update(self):
        self.controller.update_view()

    @classmethod
    def reset_instance(cls):
        """Method to reset/delete the singleton instance if needed"""
        if cls in cls._instances:
            del cls._instances[cls]

