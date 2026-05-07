# AI Agentic YouTube Comment Sentiment Analysis System

## 📌 Project Overview

This project is an AI-powered YouTube sentiment analysis system that automatically collects comments from the latest uploaded videos of a YouTube channel, performs sentiment analysis using Hugging Face Transformers, stores structured data in SQLite, and visualizes insights through a Streamlit dashboard.

---

## 🚀 Features

- Fetch latest YouTube videos using YouTube Data API
- Extract top-level comments automatically
- Perform AI-based sentiment analysis
- Store data in SQLite database
- Generate CSV reports
- Interactive Streamlit dashboard
- Video-wise sentiment summaries

---

## 🛠️ Technologies Used

- Python
- YouTube Data API v3
- Hugging Face Transformers
- SQLite
- Pandas
- Streamlit
- NLP
- Sentiment Analysis

---

## 📂 Project Structure

```text
youtube-sentiment-project/
│
├── main.py
├── youtube_api.py
├── sentiment.py
├── database.py
├── dashboard.py
├── README.md
├── requirements.txt
├── video_summary.csv
├── comments_with_sentiment.csv
└── Screenshots/
```

---

## ⚙️ How to Run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run main pipeline

```bash
python main.py
```

### Run dashboard

```bash
streamlit run dashboard.py
```

---

## 📊 Outputs

- SQLite Database
- CSV Reports
- Sentiment Dashboard
- Video-wise Analytics

---

## 🎯 Business Use Cases

- Audience sentiment tracking
- Brand monitoring
- Content performance analysis
- Marketing feedback analysis
- Social media analytics

---

## 👨‍💻 Author

Shrinidhi Seshan