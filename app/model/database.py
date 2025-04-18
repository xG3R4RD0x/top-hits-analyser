import sqlite3


class DatabaseConnection:
    _instance = None

    def __new__(cls, db_name="app_data.db"):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._db_name = db_name
            cls._instance._connection = sqlite3.connect(
                db_name, check_same_thread=False
            )
        return cls._instance

    def get_connection(self):
        """Return the SQLite connection."""
        return self._connection

    def close_connection(self):
        """Close the SQLite connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
