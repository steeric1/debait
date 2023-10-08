from dataclasses import dataclass
from users import User
import db


@dataclass
class Subscription:
    user: User
    tag: str

    @staticmethod
    def create(tag: str, user: User):
        query = """INSERT INTO subscriptions (user_id, tag) VALUES (:user_id, :tag)"""
        db.execute(query, {"user_id": user.id, "tag": tag})
        db.commit()

    @staticmethod
    def delete(tag: str, user: User):
        query = """DELETE FROM subscriptions WHERE tag=:tag AND user_id=:user_id"""
        db.execute(query, {"tag": tag, "user_id": user.id})
        db.commit()

    @staticmethod
    def is_subscribed(user: User, tag: str) -> bool:
        query = """SELECT 1 FROM subscriptions WHERE user_id=:user_id AND tag=:tag"""
        result = db.execute(query, {"user_id": user.id, "tag": tag})
        
        return result.fetchone()
