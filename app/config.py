"""Provides the configuration for the Social Insecurity application.

This file is used to set the configuration for the application.

Example:
    from flask import Flask
    from app.config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    # Use the configuration
    secret_key = app.config["SECRET_KEY"]
"""

import os

# TODO: I should probably use this to prevent clickjacking
from flask import Flask, make_response # Madeleine: add make_response to mitigate clickjacking attacks

app = Flask(__name__)

@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response



class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret"  # TODO: Use this with wtforms
    SQLITE3_DATABASE_PATH = "sqlite3.db"  # Path relative to the Flask instance folder
    UPLOADS_FOLDER_PATH = "uploads"  # Path relative to the Flask instance folder
    ALLOWED_EXTENSIONS = {}  # TODO: Might use this at some point, probably don't want people to upload any file type
    WTF_CSRF_ENABLED = True  # TODO: I should probably implement this wtforms feature, but it's not a priority

# Madeleine
# Implement wtforms CSRF protection to mitigate CSRF attacks
# Implement clickjacking protection to mitigate clickjacking attacks
# Implement SECRRET_KEY to mitigate session hijacking attacks
# Implement session cookies to mitigate session hijacking attacks
# Implement password hashing to mitigate password attacks

# Flask Login (session cookies)
# Werkzeug Security (password hashing)