import sqlite3

# Connect to SQLite database (create if it doesn't exist)
conn = sqlite3.connect("./posts.db")
c = conn.cursor()

# Create table if not exists
c.execute(
    """CREATE TABLE IF NOT EXISTS posts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              source TEXT,
              title TEXT,
              asset_url TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"""
)

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()
