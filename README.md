# debait

## Currently implemented features

* Registering, logging in and out
* Browsing tags
* Creating posts on tags and reading them
* Commenting posts
* Upvoting and downvoting posts
* Subscribing and unsubscribing to tags
* Showing posts from subscribed tags

## How to run

**Note:** This application is not testable in production (not yet, anyway).

*Prerequisite*: A PostgreSQL instance running. Create the schema for this application using `init_db.sql`

Install dependencies:
```
pip install -r requirements.txt
```

Create an `.env` file with the following variables defined:
* `DATABASE_URL` for the URL of your PostgreSQL database
* `SECRET_KEY` for the secret key of the Flask application

Run the application with
```
flask --app src/app.py run
```

### Note about NPM

I used NPM in this project for Tailwind CSS and Flowbite. However, it's practically only a development dependency, and you do not need to install the NPM dependencies of the project to run it.

## Initial plan (a lot of this I didn't have time for)

An online forum for debating and discussing various topics.
* Users can start discussion threads with a tag. This tag determines the space in which the thread is stored in the application. A tag is essentially a channel.
* Users can scroll through threads that belong to a certain tag. Threads can be upvoted and downvoted.
* Users can read threads and send messages to them. Messages can be upvoted and downvoted.
* Thread authors (OPs) are admins in their own threads. They can pin messages and delete them.
* Thread authors can also modify the title and initial post of the thread. The edits will, however, be tracked and visible to everyone reading the thread for transparency.
* Users can create accounts and log in and out. This is a requirement for interacting.
* Users can subscribe to tags and threads in these tags will appear in their personal feeds. (Some kind of recommendation algorithm?)
* Users can scroll through a list of popular tags. They can also search tags and threads globally and within a tag.
* Admin users who have permissions to delete messages and threads and ban users from engaging in a thread or a tag.
* About me page and profile view? Viewing user activity for transparency?
* Other fun stuff such as markdown support, embeds (at least images), interactive elements such as polls?

