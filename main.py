from youtube_api import (
    get_channel_id,
    get_uploads_playlist,
    get_videos,
    get_comments
)

from sentiment import analyze_sentiment
from database import (
    connect_db,
    create_tables,
    insert_video,
    insert_comment
)

import pandas as pd


def run():

    # =========================
    # USER INPUT
    # =========================

    channel_name = input("Enter YouTube Channel Name: ")

    # =========================
    # DATABASE SETUP
    # =========================

    conn = connect_db()

    create_tables(conn)

    # =========================
    # FETCH CHANNEL DATA
    # =========================

    print("\nGetting channel ID...")

    channel_id = get_channel_id(channel_name)

    print("Getting uploads playlist...")

    playlist_id = get_uploads_playlist(channel_id)

    print("Fetching latest videos...")

    videos = get_videos(playlist_id)

    print("\nProcessing videos & comments...\n")

    # =========================
    # PROCESS VIDEOS
    # =========================

    for video in videos:

        print(f"🎥 Video: {video['title']}")

        # Insert video into database
        insert_video(conn, video)

        # =========================
        # FETCH COMMENTS
        # =========================

        try:

            comments = get_comments(video["video_id"])

        except Exception as e:

            print("❌ Error fetching comments:", e)

            comments = []

        print(f"💬 Comments fetched: {len(comments)}")

        # =========================
        # PROCESS COMMENTS
        # =========================

        for c in comments:

            try:

                text = c["text"]

                # Skip empty comments
                if not text.strip():
                    continue

                # Sentiment analysis
                label, score = analyze_sentiment(text)

                # Store comment
                insert_comment(
                    conn,
                    c,
                    video["video_id"],
                    label,
                    score
                )

            except Exception as e:

                print("❌ Error processing comment:", e)

        print("-" * 60)

    # =========================
    # LOAD DATA FOR REPORTING
    # =========================

    print("\n✅ Data stored in database successfully!")

    df = pd.read_sql_query(
        "SELECT * FROM comments",
        conn
    )

    # =========================
    # VIDEO-WISE SUMMARY
    # =========================

    video_summary = (
        df.groupby(
            ["video_id", "sentiment_label"]
        )
        .size()
        .unstack(fill_value=0)
    )

    print("\n📊 Video-wise Sentiment Summary:\n")

    print(video_summary)

    # =========================
    # CHANNEL-WISE SUMMARY
    # =========================

    positive = len(
        df[df["sentiment_label"] == "POSITIVE"]
    )

    negative = len(
        df[df["sentiment_label"] == "NEGATIVE"]
    )

    total = len(df)

    print("\n📈 Channel-wise Sentiment Summary\n")

    print(f"Total Comments: {total}")

    print(f"Positive Comments: {positive}")

    print(f"Negative Comments: {negative}")

    if total > 0:

        print(
            f"Positive Percentage: "
            f"{(positive / total) * 100:.2f}%"
        )

        print(
            f"Negative Percentage: "
            f"{(negative / total) * 100:.2f}%"
        )

    # =========================
    # EXPORT CSV FILES
    # =========================

    video_summary.to_csv(
        "video_summary.csv"
    )

    df.to_csv(
        "comments_with_sentiment.csv",
        index=False
    )

    print("\n✅ CSV files exported successfully!")

    # =========================
    # CLOSE DATABASE
    # =========================

    conn.close()

    print("\n🎉 Project Execution Completed!")


# =========================
# MAIN ENTRY POINT
# =========================

if __name__ == "__main__":

    run()