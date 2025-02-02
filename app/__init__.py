"""
Provides the app package for the Social Insecurity application.
The package contains the Flask app and all of the extensions and routes.
"""

from pathlib import Path
from typing import cast

from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from app.config import Config
from app.database import SQLite3

# Instantiate and configure the app
app = Flask(__name__)
app.config.from_object(Config)

# Instantiate the sqlite database extension
sqlite = SQLite3(app, schema="schema.sql")

# Set up login management with flask_login
login = LoginManager(app)
login.login_view = 'login'  # Specify the login view
# Make sure there is a 'login' view function somewhere in your application

# Secure password storage using Bcrypt
bcrypt = Bcrypt(app)

# Enable CSRF protection
csrf = CSRFProtect(app)

# Create the instance and upload folder if they do not exist
with app.app_context():
    instance_path = Path(app.instance_path)
    if not instance_path.exists():
        instance_path.mkdir(parents=True, exist_ok=True)
    upload_path = instance_path / cast(str, app.config["UPLOADS_FOLDER_PATH"])
    if not upload_path.exists():
        upload_path.mkdir(parents=True, exist_ok=True)

# Import the routes after the app is configured
from app import routes  # noqa: E402,F401
