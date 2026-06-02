from app.controller.update_db_controller import UpdateDBController
from app.model.playlists import Playlists
from app.model.songs import Songs


class UnifiedController(UpdateDBController):

    def register_events(self):
        self.view.register_event_handler("navigate_to", self.handle_navigation)
        self.view.register_event_handler(
            "cancel_update_operation", self.cancel_update_operation
        )
        self.view.register_event_handler("start_update", self.start_update_process)
        self.view.register_event_handler("fetch_urls", self.fetch_songs_urls)
        self.view.register_event_handler("download_songs", self.download_songs)
        self.view.register_event_handler("fetch_playlist_songs", self.fetch_playlist_songs)

    def update_view(self):
        playlists = Playlists.list_playlists()
        if not playlists:
            self.view.load_data([])
            return
        all_songs = Songs.list_songs()
        data = [(pl, [s for s in all_songs if s.playlist_id == pl.playlist_id]) for pl in playlists]
        self.view.load_data(data)
