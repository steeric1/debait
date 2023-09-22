from flask import Flask
from users import User


def register(app: Flask):
    @app.route("/")
    def index():
        User.current()
        return "hello worldou"
