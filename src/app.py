from flask import Flask
import routes
import db
from dotenv import dotenv_values


def create_app():
    app = Flask(__name__)
    app.secret_key = dotenv_values(".env")["SECRET_KEY"]

    db.connect(app)
    routes.register(app)

    return app


app = create_app()
