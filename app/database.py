from __future__ import annotations

import sqlite3
from os import PathLike
from pathlib import Path
from typing import Any, Optional, cast

from flask import Flask, current_app, g


class SQLite3:
    def __init__(self, app: Optional[Flask] = None, *, path: Optional[PathLike | str] = None, schema: Optional[PathLike | str] = None) -> None:
        """Initializes the extension with optional Flask app, path, and schema."""
        if app is not None:
            self.init_app(app, path=path, schema=schema)

    def init_app(self, app: Flask, *, path: Optional[PathLike | str] = None, schema: Optional[PathLike | str] = None) -> None:
        """Initializes the extension with a Flask app, path, and schema."""
        if not hasattr(app, "extensions"):
            app.extensions = {}

        if "sqlite3" not in app.extensions:
            app.extensions["sqlite3"] = self
        else:
            raise RuntimeError("Flask SQLite3 extension already initialized")

        if path == ":memory:" or app.config.get("SQLITE3_DATABASE_PATH") == ":memory:":
            raise ValueError("Cannot use in-memory database with Flask SQLite3 extension")

        if path:
            self._path = Path(app.instance_path) / path
        elif "SQLITE3_DATABASE_PATH" in app.config:
            self._path = Path(app.instance_path) / app.config["SQLITE3_DATABASE_PATH"]
        else:
            self._path = Path(app.instance_path) / "sqlite3.db"

        if not self._path.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)

        if schema:
            with app.app_context():
                self._init_database(schema)
        app.teardown_appcontext(self._close_connection)

    @property
    def connection(self) -> sqlite3.Connection:
        """Returns the connection to the SQLite3 database."""
        conn = getattr(g, "flask_sqlite3_connection", None)
        if conn is None:
            conn = g.flask_sqlite3_connection = sqlite3.connect(self._path)
            conn.row_factory = sqlite3.Row
        return conn

    def query(self, query: str, one: bool = False, params: Optional[tuple] = None) -> Any:
        """Executes a query using prepared statements."""
        try:
            cursor = self.connection.execute(query, params or ())
            response = cursor.fetchone() if one else cursor.fetchall()
            cursor.close()
            self.connection.commit()
            return response
        except sqlite3.DatabaseError as e:
            # Log the error, for example: app.logger.error(f"Database error: {e}")
            raise

    # Specific query methods example
    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """Gets a user by their ID."""
        return self.query("SELECT * FROM Users WHERE id = ?", one=True, params=(user_id,))

    def _init_database(self, schema: PathLike | str) -> None:
        """Initializes the database with the supplied schema if it does not exist yet."""
        with current_app.open_resource(str(schema), mode="r") as file:
            self.connection.executescript(file.read())
            self.connection.commit()

    def _close_connection(self, exception: Optional[BaseException] = None) -> None:
        """Closes the connection to the database."""
        conn = cast(sqlite3.Connection, getattr(g, "flask_sqlite3_connection", None))
        if conn is not None:
            conn.close()
