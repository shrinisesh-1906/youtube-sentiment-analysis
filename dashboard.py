import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="YouTube Sentiment Dashboard",
    layout="wide"
)

st.title("📊 YouTube Comment Sentiment Dashboard")

# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect("youtube_sentiment.db")

df = pd.read_sql_query(
    "SELECT * FROM comments",
    conn
)

# ==========================================
# CHECK EMPTY DATA
# ==========================================

if df.empty:

    st.warning("No data available.")

    st.stop()

# ==========================================
# KPI METRICS
# ==========================================

total_comments = len(df)

positive_count = len(
    df[df["sentiment_label"] == "POSITIVE"]
)

negative_count = len(
    df[df["sentiment_label"] == "NEGATIVE"]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Comments",
    total_comments
)

col2.metric(
    "Positive Comments",
    positive_count
)

col3.metric(
    "Negative Comments",
    negative_count
)

st.divider()

# ==========================================
# PIE CHART
# ==========================================

st.subheader("📈 Sentiment Distribution")

sentiment_counts = (
    df["sentiment_label"]
    .value_counts()
)

fig, ax = plt.subplots()

ax.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct="%1.1f%%"
)

st.pyplot(fig)

st.divider()

# ==========================================
# VIDEO FILTER
# ==========================================

st.subheader("🎥 Video-wise Analysis")

video_ids = df["video_id"].unique()

selected_video = st.selectbox(
    "Select Video ID",
    video_ids
)

video_df = df[
    df["video_id"] == selected_video
]

st.write(video_df)

st.divider()

# ==========================================
# SENTIMENT SUMMARY TABLE
# ==========================================

st.subheader("📋 Sentiment Summary Table")

summary = (
    df.groupby(
        ["video_id", "sentiment_label"]
    )
    .size()
    .unstack(fill_value=0)
)

st.dataframe(summary)

# ==========================================
# RAW DATA
# ==========================================

st.subheader("🗂 Raw Comments Data")

st.dataframe(df)

conn.close()