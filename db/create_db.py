import sqlite3

# Connect to SQLite database (create if it doesn't exist)
conn = sqlite3.connect("./db/posts.db")
c = conn.cursor()

# Create table if not exists
c.execute(
    """CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              source TEXT,
              title TEXT,
              image_url TEXT,
              timestamp DATETIME)"""
)

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()
