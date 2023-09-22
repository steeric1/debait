from flask import Flask, render_template, redirect, request, url_for
from users import User
import base64


def register(app: Flask):
    @app.route("/")
    def index():
        user = User.current()
        print(user)
        return render_template("index.html", user=user)

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/login", methods=["POST"])
    def handle_login():
        form = request.form

        if not all([form["username"], form["password"]]):
            return render_template("login.html", error="All required fields were not provided."), 400

        if User.login(form["username"], form["password"]):
            return redirect("/")
        else:
            return render_template("login.html", error="Incorrect username or password.")

    @app.route("/register")
    def register():
        return render_template("register.html")
    
    @app.route("/register", methods=["POST"])
    def handle_register():
        form = request.form
        error = None

        if not all([form["username"], form["password"], form["confirm-password"]]):
            error = "All required fields were not provided."
        else:
            username, password, confirm_password = form["username"], form["password"], form["confirm-password"]

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


def encode_param(param: str):
    return base64.b64encode(param.encode())


def decode_param(param: bytes):
    try:
        decoded = base64.b64decode(param).decode()
    except:
        decoded = "" 

    return decoded