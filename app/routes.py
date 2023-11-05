from pathlib import Path

from flask import flash, redirect, render_template, send_from_directory, url_for

from app import app, sqlite
from app.forms import CommentsForm, FriendsForm, IndexForm, PostForm, ProfileForm

# Index route
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    index_form = IndexForm()
    login_form = index_form.login
    register_form = index_form.register

    if login_form.is_submitted() and login_form.submit.data:
        user = sqlite.get_user_by_username(login_form.username.data) # Refactored to use parameterized query

        if user is None:
            flash("Sorry, this user does not exist!", category="warning")
        elif user["password"] != login_form.password.data:
            flash("Sorry, wrong password!", category="warning")
        elif user["password"] == login_form.password.data:
            return redirect(url_for("stream", username=login_form.username.data))

    elif register_form.is_submitted() and register_form.submit.data:
        sqlite.create_user(register_form.username.data, register_form.first_name.data, register_form.last_name.data, register_form.password.data) # Refactored to use parameterized query
        flash("User successfully created!", category="success")
        return redirect(url_for("index"))

    return render_template("index.html.j2", title="Welcome", form=index_form)

# Stream route
@app.route("/stream/<string:username>", methods=["GET", "POST"])
def stream(username: str):
    post_form = PostForm()
    user = sqlite.get_user_by_username(username) # Refactored to use parameterized query

    if post_form.is_submitted():
        if post_form.image.data:
            path = Path(app.instance_path) / app.config["UPLOADS_FOLDER_PATH"] / post_form.image.data.filename
            post_form.image.data.save(path)

        sqlite.create_post(user["id"], post_form.content.data, post_form.image.data.filename) # Refactored to use parameterized query
        return redirect(url_for("stream", username=username))

    posts = sqlite.get_user_posts_and_friends(user["id"]) # Refactored to use parameterized query
    return render_template("stream.html.j2", title="Stream", username=username, form=post_form, posts=posts)

# Comments route
@app.route("/comments/<string:username>/<int:post_id>", methods=["GET", "POST"])
def comments(username: str, post_id: int):
    comments_form = CommentsForm()
    user = sqlite.get_user_by_username(username) # Refactored to use parameterized query

    if comments_form.is_submitted():
        sqlite.create_comment(post_id, user["id"], comments_form.comment.data) # Refactored to use parameterized query

    post = sqlite.get_post_by_id(post_id) # Refactored to use parameterized query
    comments = sqlite.get_comments_by_post_id(post_id) # Refactored to use parameterized query
    return render_template(
        "comments.html.j2", title="Comments", username=username, form=comments_form, post=post, comments=comments
    )

# Friends route
@app.route("/friends/<string:username>", methods=["GET", "POST"])
def friends(username: str):
    friends_form = FriendsForm()
    user = sqlite.get_user_by_username(username) # Refactored to use parameterized query

    if friends_form.is_submitted():
        friend = sqlite.get_user_by_username(friends_form.username.data) # Refactored to use parameterized query
        friends = sqlite.get_friends_by_user_id(user["id"]) # Refactored to use parameterized query

        if friend is None:
            flash("User does not exist!", category="warning")
        elif friend["id"] == user["id"]:
            flash("You cannot be friends with yourself!", category="warning")
        elif friend["id"] in [f["f_id"] for f in friends]:
            flash("You are already friends with this user!", category="warning")
        else:
            sqlite.create_friendship(user["id"], friend["id"]) # Refactored to use parameterized query
            flash("Friend successfully added!", category="success")

    friends = sqlite.get_friends_by_user_id(user["id"]) # Refactored to use parameterized query
    return render_template("friends.html.j2", title="Friends", username=username, friends=friends, form=friends_form)

# Profile route
@app.route("/profile/<string:username>", methods=["GET", "POST"])
def profile(username: str):
    profile_form = ProfileForm()
    user = sqlite.get_user_by_username(username) # Refactored to use parameterized query

    if profile_form.is_submitted():
        sqlite.update_user_profile(username, profile_form) # Refactored to use parameterized query
        return redirect(url_for("profile", username=username))

    return render_template("profile.html.j2", title="Profile", username=username, user=user, form=profile_form)

# Uploads route
@app.route("/uploads/<string:filename>")
def uploads(filename):
    return send_from_directory(Path(app.instance_path) / app.config["UPLOADS_FOLDER_PATH"], filename)
