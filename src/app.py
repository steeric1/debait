from flask import Flask
import routes
import db


def create_app():
    app = Flask(__name__)

    db.connect(app)
    routes.register(app)

    return app


app = create_app()
