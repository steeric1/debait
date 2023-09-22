from uuid import UUID
from flask import session
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
            query = """SELECT (name) FROM users WHERE true"""
            result = db.execute(query)

            name = result.fetchone()
            if name:
                return User(curr_id, name)
        
        return None
