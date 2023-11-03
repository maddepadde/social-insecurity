# Madeleine:
# created file app/models.py
# created class User

# Madeleine:
# password hashing and verification

from werkzeug.security import generate_password_hash, check_password_hash

# Madeleine:
# datetime
from datetime import datetime

# Madeleine:
# login manager
from flask_login import UserMixin # UserMixin provides default implementations for the methods that Flask-Login expects user objects to have
from app import login

# Madeleine:
# database
from app.database import SQLite3

db = SQLite3()

# Madeleine:
# create a user class

class User(UserMixin, db.Model):
    # create a table called users
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # first name is a string
    first_name = db.Column(db.String(64), index=True)
    # last name is a string
    last_name = db.Column(db.String(64), index=True)
    # email is unique
    email = db.Column(db.String(120), index=True, unique=True)
    # password is hashed
    password_hash = db.Column(db.String(128))
    # posts is a relationship
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # TODO: Madeleine: add profile stuff

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
class Posts(UserMixin, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    # Madeleine:
    # body is a string
    body = db.Column(db.String(140))
    # Madeleine:
    # timestamp is a datetime
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Madeleine:
    # user_id is an integer
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)
    