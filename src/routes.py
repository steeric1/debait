from flask import Flask, render_template, redirect, request, abort
from users import User
from posts import Post
from comments import Comment
from votes import Vote
from subscriptions import Subscription
from typing import List


def register(app: Flask):
    @app.get("/")
    def index():
        return redirect("/general")

    @app.get("/general")
    def general():
        (posts, vote_scores, user_votes, num_comments, _) = get_tag_data("general")
        return render_template(
            "index.html",
            active="general",
            tag="general",
            posts=posts,
            subscribable=False,
            back_to_from_post="/general",
            back_to_from_post_display="General",
            user=User.current(),
            vote_scores=vote_scores,
            user_votes=user_votes,
            num_comments=num_comments,
        )

    @app.get("/subscribed")
    def subscribed():
        user = User.current()
        if user is None:
            return redirect("/general")

        posts = Subscription.subscribed_posts(user)
        vote_scores, user_votes, num_comments = get_posts_data(posts)

        return render_template(
            "index.html",
            active="subscribed",
            header=False,
            show_post_tag=True,
            back_to_from_post="/subscribed",
            back_to_from_post_display="Subscribed",
            posts=posts,
            user=User.current(),
            vote_scores=vote_scores,
            user_votes=user_votes,
            num_comments=num_comments,
        )

    @app.get("/login")
    def login():
        if User.current() is not None:
            return redirect("/")

        return render_template("login.html")

    @app.post("/login")
    def handle_login():
        redirect_to = request.args.get("redirect_to", "/")
        form = request.form

        if not all([form["username"], form["password"]]):
            return (
                render_template(
                    "login.html", error="All required fields were not provided."
                ),
                400,
            )

        if User.login(form["username"], form["password"]):
            return redirect(f"{redirect_to}")
        else:
            return render_template(
                "login.html", error="Incorrect username or password."
            )

    @app.get("/register")
    def register():
        return render_template("register.html")

    @app.post("/register")
    def handle_register():
        form = request.form
        error = None

        if not all([form["username"], form["password"], form["confirm-password"]]):
            error = "All required fields were not provided."
        else:
            username, password, confirm_password = (
                form["username"],
                form["password"],
                form["confirm-password"],
            )

            if password != confirm_password:
                error = "The passwords do not match."
            elif User.get_by_name(username) is not None:
                error = "A username by that name exists already."

        if error:
            return render_template("register.html", error=error), 400
        else:
            User.create(username, password)
            User.login(username, password)

            return redirect("/")

    @app.post("/logout")
    def logout():
        User.logout()
        return redirect("/")

    @app.get("/tag/<tag>")
    def tag(tag: str):
        posts, vote_scores, user_votes, num_comments, subscribed = get_tag_data(tag)
        return render_template(
            "tag.html",
            tag=tag,
            posts=posts,
            user=User.current(),
            vote_scores=vote_scores,
            user_votes=user_votes,
            num_comments=num_comments,
            subscribed=subscribed,
        )

    @app.get("/post/<id>")
    def post_get(id: int):
        post = Post.get_by_id(id)
        if post:
            comments = Comment.comments_to_post(post.id)
            return render_template(
                "post.html", post=post, user=User.current(), comments=comments
            )

        abort(404)

    @app.post("/post/<tag>")
    def post_post(tag: str):
        user = User.current()
        if not user:
            abort(403)

        form = request.form

        if not all([form["title"], form["content"]]):
            abort(400)

        title, content = form["title"], form["content"]

        Post.create(tag, title, content, user)
        return ""

    @app.post("/comment/<post_id>")
    def comment(post_id: int):
        user = User.current()
        if not user:
            abort(403)

        form = request.form
        if not form["content"]:
            abort(400)

        Comment.create(post_id, form["content"], user)
        return ""

    @app.post("/upvote/<post_id>")
    def upvote(post_id: int):
        user = User.current()
        if not user:
            abort(403)

        if Post.get_by_id(post_id):
            Vote.upvote(post_id, user)
        else:
            abort(400)

        return ""

    @app.delete("/upvote/<post_id>")
    def delete_upvote(post_id: int):
        user = User.current()
        if not user:
            abort(403)

        Vote.delete(post_id, user)
        return ""

    @app.post("/downvote/<post_id>")
    def downvote(post_id: int):
        user = User.current()
        if not user:
            abort(403)

        Vote.downvote(post_id, user)
        return ""

    @app.delete("/downvote/<post_id>")
    def delete_downvote(post_id: int):
        user = User.current()
        if not user:
            abort(403)

        Vote.delete(post_id, user)
        return ""

    @app.post("/subscribe/<tag>")
    def subscribe(tag: str):
        if tag == "general":
            abort(404)

        user = User.current()
        if not user:
            abort(403)

        Subscription.create(tag, user)
        return ""

    @app.delete("/subscribe/<tag>")
    def unsubscribe(tag: str):
        if tag == "general":
            abort(404)

        user = User.current()
        if not user:
            abort(403)

        Subscription.delete(tag, user)
        return ""


def get_tag_data(tag: str):
    posts = Post.get_posts(tag)
    vote_scores, user_votes, num_comments = get_posts_data(posts)

    user = User.current()
    subscribed = Subscription.is_subscribed(user, tag) if user else False

    return posts, vote_scores, user_votes, num_comments, subscribed


def get_posts_data(posts: List[Post]):
    vote_scores = {
        post_id: Vote.calculate(post_id) for post_id in map(lambda post: post.id, posts)
    }

    user = User.current()
    user_votes = (
        {
            post_id: Vote.get_user_vote(post_id, user)
            for post_id in map(lambda post: post.id, posts)
        }
        if user
        else None
    )

    num_comments = {
        post_id: len(Comment.comments_to_post(post_id))
        for post_id in map(lambda post: post.id, posts)
    }

    return vote_scores, user_votes, num_comments
