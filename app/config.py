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


class Config:
    # Ensure that the secret key is set in the environment, otherwise raise an error
    if not os.environ.get("SECRET_KEY"):
        raise ValueError("No SECRET_KEY set for Flask application")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    
    SQLITE3_DATABASE_PATH = "sqlite3.db"  # Path relative to the Flask instance folder
    UPLOADS_FOLDER_PATH = "uploads"  # Path relative to the Flask instance folder
    
    # Define allowed file extensions (e.g., images, documents)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    WTF_CSRF_ENABLED = True  # Enable CSRF protection for forms
