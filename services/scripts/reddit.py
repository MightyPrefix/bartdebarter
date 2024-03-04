import os, sys, logging
import sqlite3
from dotenv import load_dotenv
from datetime import datetime, timezone
from pprint import pprint
import praw

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Access Reddit client ID and secret
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_useragent = os.getenv("REDDIT_USERAGENT")

# Check if environment variables are set
if not all([reddit_client_id, reddit_client_secret, reddit_useragent]):
    logging.error("One or more environment variables not set")
    sys.exit()

SUBREDDIT_NAME = "shitposting"

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_useragent,
)

# Get the top post from the day
top_posts = reddit.subreddit(SUBREDDIT_NAME).top(time_filter="day", limit=1)
# The PRAW 'top' method returns a generator, so we can use next to get the first post
post = next(top_posts, None)

# Get the current timestamp
current_utc_timestamp = datetime.now().timestamp()

if post is None or current_utc_timestamp - post.created_utc > 24 * 3600:
   logging.error(f"No posts found in the last 24 hours on /r/{SUBREDDIT_NAME}")
   sys.exit()

# Get the absolute path of the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '../db/posts.db')

def handle_gallery_post(post):
    media_urls = [f"https://i.reddit.it/{item['media_id']}.jpg" for item in post.gallery_data['items']]
    return ",".join(media_urls)

def handle_video_post(post):
    return post.secure_media["reddit_video"]["fallback_url"]

def handle_post(post, conn):
    source = post.permalink
    title = post.title

    # There are 4 different types of posts
    # 1. Video post => store the post.secure_media.reddit_video.fallback_url link in the db
    # 2. Gallery post => additional logic is required to obtain the individual image URLs
    # 3. Single asset post (e.g. image or gif) => store the post.url link in the db

    # Check the post type and handle accordingly
    if hasattr(post, 'is_video') and post.is_video:
        asset_url = handle_video_post(post)
    elif hasattr(post, 'is_gallery') and post.is_gallery:
        asset_url = handle_gallery_post(post)
    else:
        asset_url = post.url

    with conn:
        conn.execute(
            "INSERT INTO posts (source, title, asset_url) VALUES (?, ?, ?)",
            (source, title, asset_url),
        )

with sqlite3.connect(db_path) as conn:
    handle_post(post, conn)
