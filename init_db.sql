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

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INT,
    content TEXT,
    author_id UUID,
    commented_at timestamp,
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(author_id) REFERENCES users(uid) on DELETE SET NULL
);

CREATE TABLE votes (
    post_id INT,
    user_id UUID,
    effect INT,
    PRIMARY KEY(post_id, user_id),
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(uid) ON DELETE CASCADE
);

CREATE TABLE subscriptions (
    user_id UUID,
    tag TEXT,
    PRIMARY KEY(user_id, tag),
    FOREIGN KEY(user_id) REFERENCES users(uid) ON DELETE CASCADE
);