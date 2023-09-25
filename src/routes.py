from flask import Flask, render_template, redirect, request, abort
from users import User
from posts import Post
from comments import Comment
import base64


def register(app: Flask):
    @app.get("/")
    def index():
        user = User.current()
        print(user)
        return render_template("index.html", user=user)

    @app.get("/login")
    def login():
        if User.current() is not None:
            return redirect("/")

        return render_template("login.html")

    @app.post("/login")
    def handle_login():
        form = request.form

        if not all([form["username"], form["password"]]):
            return (
                render_template(
                    "login.html", error="All required fields were not provided."
                ),
                400,
            )

        if User.login(form["username"], form["password"]):
            return redirect("/")
        else:
            return render_template(
                "login.html", error="Incorrect username or password."
            )

    @app.get("/register")
    def register():
        return render_template("register.html")

    @app.post("/register")
    def handle_register():
        form = request.form
        error = None

        if not all([form["username"], form["password"], form["confirm-password"]]):
            error = "All required fields were not provided."
        else:
            username, password, confirm_password = (
                form["username"],
                form["password"],
                form["confirm-password"],
            )

            if password != confirm_password:
                error = "The passwords do not match."
            elif User.get_by_name(username) is not None:
                error = "A username by that name exists already."

        if error:
            return render_template("register.html", error=error), 400
        else:
            User.create(username, password)
            User.login(username, password)

            return redirect("/")

    @app.post("/logout")
    def logout():
        User.logout()
        return redirect("/")

    @app.get("/browse")
    def browse():
        tag = request.args.get("tag")
        if tag:
            posts = Post.get_posts(tag)
            print(posts)
            return render_template(
                "tag.html", tag=tag, posts=posts, user=User.current()
            )

        abort(404)

    @app.get("/post/<id>")
    def post_get(id: int):
        post = Post.get_by_id(id)
        if post:
            comments = Comment.comments_to_post(post.id)
            return render_template(
                "post.html", post=post, user=User.current(), comments=comments
            )

        abort(404)

    @app.post("/post/<tag>")
    def post_post(tag: str):
        user = User.current()
        if not user:
            abort(403)

        form = request.form

        if not all([form["title"], form["content"]]):
            abort(400)

        title, content = form["title"], form["content"]

        Post.create(tag, title, content, user)
        return ""

    @app.post("/comment/<post_id>")
    def comment(post_id: int):
        user = User.current()
        if not user:
            abort(403)

        form = request.form
        if not form["content"]:
            abort(400)

        Comment.create(post_id, form["content"], user)
        return ""


def encode_param(param: str):
    return base64.b64encode(param.encode())


def decode_param(param: bytes):
    try:
        decoded = base64.b64decode(param).decode()
    except:
        decoded = ""

    return decoded
