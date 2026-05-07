import streamlit as st
import pandas as pd
import sqlite3

# Page title
st.title("📊 YouTube Sentiment Analysis Dashboard")

# Connect database
conn = sqlite3.connect("youtube_sentiment.db")

# Load data
comments_df = pd.read_sql_query(
    "SELECT * FROM comments",
    conn
)

videos_df = pd.read_sql_query(
    "SELECT * FROM videos",
    conn
)

# Overview metrics
st.subheader("📌 Overview")

total_comments = len(comments_df)
positive = len(comments_df[comments_df["sentiment_label"] == "POSITIVE"])
negative = len(comments_df[comments_df["sentiment_label"] == "NEGATIVE"])

col1, col2, col3 = st.columns(3)

col1.metric("Total Comments", total_comments)
col2.metric("Positive Comments", positive)
col3.metric("Negative Comments", negative)

# Sentiment distribution
st.subheader("📈 Sentiment Distribution")

sentiment_counts = comments_df["sentiment_label"].value_counts()

st.bar_chart(sentiment_counts)

# Video-wise summary
st.subheader("🎥 Video-wise Sentiment Summary")

video_summary = (
    comments_df.groupby(
        ["video_id", "sentiment_label"]
    )
    .size()
    .unstack(fill_value=0)
)

st.dataframe(video_summary)

# Raw comments
st.subheader("💬 Comments Data")

st.dataframe(comments_df)