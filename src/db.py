from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import dotenv_values


db = None


def connect(app: Flask):
    global db

    app.config["SQLALCHEMY_DATABASE_URI"] = dotenv_values(".env")["DATABASE_URL"]
    db = SQLAlchemy(app)


def execute(query: str, values: dict = {}):
    return db.session.execute(text(query), values)


def commit():
    db.session.commit()
