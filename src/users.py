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

        user_id = result.fetchone()
        if user_id:
            return User(user_id, name)
        else:
            return None

    @staticmethod
    def create(username: str, password: str):
        hash = generate_password_hash(password)
        user_id = uuid4()

        query = """INSERT INTO users (uid, name, password) VALUES (:uuid, :username, :password)"""
        db.execute(query, {"uuid": user_id, "username": username, "password": hash})
        db.commit()

        return User(user_id, username)


    @staticmethod
    def login(user_id: UUID):
        session["user_id"] = user_id
        
