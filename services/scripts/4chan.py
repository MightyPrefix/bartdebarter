import os, sys, logging
import requests
import sqlite3
from dotenv import load_dotenv
from datetime import datetime

# Define the subreddit 
SUBREDDIT = 'g'

# Get the absolute path of the directory containing the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "../db/posts.db")

# Function to get the top post in a subreddit
def get_top_post(subreddit):
    url = f"https://a.4cdn.org/{subreddit}/catalog.json"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Extracting the top post
        if data:
            # Assuming the first page
            threads = data[0]['threads']  
            top_thread = max(threads, key=lambda x: x.get('replies', 0))
            
            # Extracting relevant information
            title = top_thread.get('sub', '')
            image_url = ""
            post_number = top_thread.get('no')
            replies = top_thread.get('replies', 0)
            images = top_thread.get('images', 0)
            
            # Getting image URL if available
            if images > 0 and 'tim' in top_thread and 'ext' in top_thread:
                image_url = f"https://i.4cdn.org/{subreddit}/{top_thread['tim']}{top_thread['ext']}"
            
            post_link = f"https://boards.4chan.org/{subreddit}/thread/{post_number}"
            
            return title, image_url, post_link
        else:
            return None, None, None
    except Exception as e:
        print("Error:", e)
        return None, None, None

def insert_post(source, title, asset_url, conn):

    with conn:
        conn.execute(
            "INSERT INTO posts (source, title, asset_url) VALUES (?, ?, ?)",
            (source, title, asset_url),
        )

# Example usage
if __name__ == "__main__":
    title, image_url, post_link = get_top_post(SUBREDDIT)
    if title:
        print("Top Post:")
        print("Title:", title)
        print("Image URL:", image_url)
        print("Post Link:", post_link)
        with sqlite3.connect(db_path) as conn:
            insert_post(post_link, title, image_url, conn)

        
    else:
        print("No posts found or error occurred.")