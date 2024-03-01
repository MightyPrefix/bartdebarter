import os
import sqlite3
from dotenv import load_dotenv
from datetime import datetime, timezone
import praw

# Load environment variables from .env file
load_dotenv()

# Access Reddit client ID and secret
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_useragent = os.getenv("REDDIT_USERAGENT")

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_useragent,
)

# Connect to the SQLite db
conn = sqlite3.connect("../db/posts.db")
c = conn.cursor()

# Get the top post from the day
post = reddit.subreddit("shitposting").top(time_filter='day', limit=1)[0]

# Get current UTC timestamp
current_utc_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()

# Make sure the post is from today
if current_utc_timestamp - post.created_utc < 24 * 3600:
    # Extract post title
    title = post.title

    # Extract image URLs from the gallery (assuming there are two images)
    image_urls = [image["url"] for image in post.gallery_data["items"]]

    # Insert data into the database
    c.execute(
        "INSERT INTO posts (title, image_url1, image_url2) VALUES (?, ?, ?)",
        (title, *image_urls),
    )

    # Save (commit) the changes
    conn.commit()

# Close the connection
conn.close()
