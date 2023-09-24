CREATE TABLE users (
    uid UUID PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    tag TEXT,
    title TEXT,
    content TEXT,
    author_id UUID,
    posted_at timestamp,
    FOREIGN KEY(author_id) REFERENCES users(uid) ON DELETE SET NULL
);