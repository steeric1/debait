from dataclasses import dataclass
from datetime import datetime
from users import User
import db


POST_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


@dataclass
class Post:
    id: int
    tag: str
    title: str
    content: str
    author: User
    timestamp: datetime

    @staticmethod
    def get_posts(tag: str):
        query = """SELECT id, tag, title, content, author_id, posted_at FROM posts WHERE tag=:tag"""
        result = db.execute(query, {"tag": tag})

        rows = result.fetchall()
        posts = list(
            map(lambda row: Post(*row[:4], User.get_by_id(row[4]), row[5]), rows)
        )

        return posts

    @staticmethod
    def create(tag: str, title: str, content: str, author: User):
        query = """
            INSERT INTO posts (tag, title, content, author_id, posted_at)
            VALUES (:tag, :title, :content, :author, :timestamp)
            """

        db.execute(
            query,
            {
                "tag": tag,
                "title": title,
                "content": content,
                "author": author.id,
                "timestamp": datetime.now().strftime(POST_TIMESTAMP_FORMAT),
            },
        )
        db.commit()

    @staticmethod
    def get_by_id(id: int):
        query = """SELECT tag, title, content, author_id, posted_at FROM posts WHERE id=:id"""
        result = db.execute(query, {"id": id})

        row = result.fetchone()
        return Post(id, *row[:3], User.get_by_id(row[3]), row[4]) if row else None
