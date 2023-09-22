from flask import Flask, render_template, redirect
from users import User


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
        return redirect("/")

    @app.route("/register")
    def register():
        return render_template("register.html")
    
    @app.route("/register", methods=["POST"])
    def handle_register():
        return redirect("/")

