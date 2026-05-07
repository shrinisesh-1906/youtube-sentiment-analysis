from youtube_api import (
    get_channel_id,
    get_uploads_playlist,
    get_videos,
    get_comments
)

from sentiment import analyze_sentiment
from database import connect_db, create_tables, insert_video, insert_comment

def run():
    channel_name = "Google Developers"

    conn = connect_db()
    create_tables(conn)

    print("Getting channel ID...")
    channel_id = get_channel_id(channel_name)

    print("Getting uploads playlist...")
    playlist_id = get_uploads_playlist(channel_id)

    print("Fetching videos...")
    videos = get_videos(playlist_id)

    print("\nProcessing videos & comments...\n")

    for video in videos:
        print("Video:", video["title"])

        insert_video(conn, video)

        comments = get_comments(video["video_id"])
        print(f"Comments fetched: {len(comments)}")

        for c in comments:
            label, score = analyze_sentiment(c["text"])
            insert_comment(conn, c, video["video_id"], label, score)

        print("-" * 50)

    print("\n✅ Data stored in database successfully!")

    # ✅ MOVE REPORTING HERE
    import pandas as pd

    df = pd.read_sql_query("SELECT * FROM comments", conn)

    video_summary = df.groupby(["video_id", "sentiment_label"]).size().unstack(fill_value=0)

    video_summary["total"] = video_summary.sum(axis=1)

    for col in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
        if col in video_summary.columns:
            video_summary[col + "_%"] = (video_summary[col] / video_summary["total"]) * 100

    print("\n📊 Video-wise Sentiment Summary:\n")
    print(video_summary)

    # Save CSV
    video_summary.to_csv("video_summary.csv")
    df.to_csv("comments_with_sentiment.csv", index=False)

    print("\n✅ CSV files exported!")
    
if __name__ == "__main__":
    run()