from app.api.spotipy import SpotifyAPIHandler as sp

class BaseController:
    """Base controller that defines the common interface for all controllers"""

    def __init__(self, main_controller):
        """
        Initialize the base controller.

        Args:
            main_controller: Reference to the main controller
        """
        print("called base controller")
        self.main_controller = main_controller
        self.view = None
        self.sp = sp()

    def set_view(self, view):
        """
        Set the view that this controller manages and register events.

        Args:
            view: The view to be managed by this controller
        """
        self.view = view
        self.register_events()

    def register_events(self):
        """
        Register events for the specific view.
        Each controller subclass should implement this method.
        """
        raise NotImplementedError("Specific controllers must implement this method")
    
    def update_view(self):
        """
        This method is called to update the view on show
        Just in case it needs to fetchs data automatically on show
        """
        pass

    def navigate_to(self, view_name):
        """
        Navigate to a specific view.

        Args:
            view_name: Name of the view to display
        """
        return self.main_controller.navigate_to(view_name)
