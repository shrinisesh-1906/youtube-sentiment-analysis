# AI Agentic YouTube Comment Sentiment Analysis System

## Overview
This project collects YouTube comments from the latest uploaded videos of a channel, performs sentiment analysis using Hugging Face transformers, stores results in SQLite, and visualizes insights using Streamlit.

## Features
- Fetch latest YouTube videos
- Extract comments using YouTube Data API
- Sentiment analysis with Hugging Face
- SQL database storage
- CSV report export
- Interactive Streamlit dashboard

## Technologies Used
- Python
- YouTube Data API v3
- Hugging Face Transformers
- SQLite
- Pandas
- Streamlit

## How to Run

### Install dependencies
pip install -r requirements.txt

### Run main pipeline
python main.py

### Run dashboard
streamlit run dashboard.py