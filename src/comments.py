from dataclasses import dataclass
from datetime import datetime
from users import User
from posts import Post
from users import User
import db


COMMENT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


@dataclass
class Comment:
    id: int
    post: Post
    author: User
    content: str
    timestamp: datetime

    @staticmethod
    def create(post_id: int, content: str, author: User):
        query = """INSERT INTO comments (post_id, content, author_id, commented_at) VALUES (:post_id, :content, :author, :commented_at)"""
        db.execute(
            query,
            {
                "post_id": post_id,
                "content": content,
                "author": author.id,
                "commented_at": datetime.now().strftime(COMMENT_TIMESTAMP_FORMAT),
            },
        )
        db.commit()

    @staticmethod
    def comments_to_post(post_id: int):
        query = """SELECT id, author_id, content, commented_at FROM comments WHERE post_id=:post_id"""
        result = db.execute(query, {"post_id": post_id})

        rows = result.fetchall()
        comments = list(
            map(
                lambda row: Comment(
                    row[0], Post.get_by_id(post_id), User.get_by_id(row[1]), *row[2:4]
                ),
                rows,
            )
        )

        return comments
