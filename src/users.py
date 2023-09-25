from uuid import UUID, uuid4
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from dataclasses import dataclass
import db


@dataclass
class User:
    id: UUID
    name: str

    @staticmethod
    def current():
        curr_id = session.get("user_id")

        if curr_id:
            query = """SELECT (name) FROM users WHERE uid=:user_id"""
            result = db.execute(query, {"user_id": curr_id})

            user = result.fetchone()
            if user:
                return User(curr_id, user[0])

        return None

    @staticmethod
    def get_by_name(name: str):
        query = """SELECT (uid) FROM users WHERE name=:name"""
        result = db.execute(query, {"name": name})

        user = result.fetchone()
        if user:
            return User(user[0], name)
        else:
            return None

    @staticmethod
    def get_by_id(id: UUID):
        query = """SELECT name FROM users WHERE uid=:uid"""
        result = db.execute(query, {"uid": id})

        row = result.fetchone()
        return User(id, row[0]) if row else None

    @staticmethod
    def create(username: str, password: str):
        hash = generate_password_hash(password)
        user_id = uuid4()

        query = """INSERT INTO users (uid, name, password) VALUES (:uuid, :username, :password)"""
        db.execute(query, {"uuid": user_id, "username": username, "password": hash})
        db.commit()

    @staticmethod
    def login(username: str, password: str):
        user = User.get_by_name(username)
        if user and check_password_hash(User.get_pwhash(user.id), password):
            session["user_id"] = user.id
            return True
        else:
            return False

    @staticmethod
    def get_pwhash(user_id: UUID):
        query = """SELECT (password) FROM users WHERE uid=:user_id"""
        result = db.execute(query, {"user_id": user_id})

        row = result.fetchone()
        return row[0] if row else None

    @staticmethod
    def logout():
        session["user_id"] = None
