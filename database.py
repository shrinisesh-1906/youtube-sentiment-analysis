import sqlite3

def connect_db():
    conn = sqlite3.connect("youtube_sentiment.db")
    return conn


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        video_id TEXT PRIMARY KEY,
        title TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        comment_id TEXT PRIMARY KEY,
        video_id TEXT,
        text TEXT,
        author TEXT,
        likes INTEGER,
        sentiment_label TEXT,
        sentiment_score REAL
    )
    """)

    conn.commit()


def insert_video(conn, video):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO videos VALUES (?, ?)
    """, (video["video_id"], video["title"]))
    conn.commit()


def insert_comment(conn, comment, video_id, label, score):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO comments VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        comment["comment_id"],
        video_id,
        comment["text"],
        comment["author"],
        comment["likes"],
        label,
        score
    ))
    conn.commit()