class BaseController:
    """Base controller that defines the common interface for all controllers"""

    def __init__(self, main_controller):
        """
        Initialize the base controller.

        Args:
            main_controller: Reference to the main controller
        """
        self.main_controller = main_controller
        self.view = None

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

    def navigate_to(self, view_name):
        """
        Navigate to a specific view.

        Args:
            view_name: Name of the view to display
        """
        return self.main_controller.navigate_to(view_name)
