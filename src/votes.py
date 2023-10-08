from dataclasses import dataclass
from users import User
from posts import Post
from uuid import UUID
import db


@dataclass
class Vote:
    post_id: int
    user_id: UUID
    effect: int

    @staticmethod
    def upvote(post_id: int, user: User):
        Vote.delete(post_id, user)

        query = """INSERT INTO votes (post_id, user_id, effect) VALUES (:post_id, :user_id, 1)"""

        db.execute(query, {"post_id": post_id, "user_id": user.id})
        db.commit()

    @staticmethod
    def downvote(post_id: int, user: User):
        Vote.delete(post_id, user)

        query = """INSERT INTO votes (post_id, user_id, effect) VALUES (:post_id, :user_id, -1)"""

        db.execute(query, {"post_id": post_id, "user_id": user.id})
        db.commit()

    @staticmethod
    def delete(post_id: int, user: User):
        query = """DELETE FROM votes WHERE post_id=:post_id AND user_id=:user_id"""

        db.execute(query, {"post_id": post_id, "user_id": user.id})
        db.commit()

    @staticmethod
    def calculate(post_id: int):
        query = """SELECT SUM(effect) FROM votes WHERE post_id=:post_id"""
        result = db.execute(query, {"post_id": post_id})

        row = result.fetchone()
        return row[0] if row[0] else 0

    @staticmethod
    def get_user_vote(post_id: int, user: User):
        query = """SELECT effect FROM votes WHERE post_id=:post_id AND user_id=:user_id"""
        result = db.execute(query, {"post_id": post_id, "user_id": user.id})

        row = result.fetchone()
        return row[0] if row else 0