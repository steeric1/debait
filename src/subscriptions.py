from dataclasses import dataclass
from users import User
from posts import Post
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

    @staticmethod
    def subscribed_posts(user: User):
        query = """
            SELECT id, posts.tag, title, content, author_id, posted_at
            FROM subscriptions
            INNER JOIN posts
                ON subscriptions.tag = posts.tag
            WHERE user_id=:user_id
            ORDER BY posted_at ASC;"""
        result = db.execute(query, {"user_id": user.id})

        rows = result.fetchall()
        posts = list(
            map(lambda row: Post(*row[:4], User.get_by_id(row[4]), row[5]), rows)
        )

        return posts
