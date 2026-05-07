import re

from transformers import pipeline


# ==========================================
# LOAD SENTIMENT MODEL (LAZY LOADING)
# ==========================================

classifier = None


def load_model():

    global classifier

    if classifier is None:

        print("Loading sentiment model...\n")

        classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )


# ==========================================
# TEXT CLEANING FUNCTION
# ==========================================

def clean_text(text):

    # Convert to string
    text = str(text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove URLs
    text = re.sub(r"http\S+", "", text)

    # Remove extra spaces/newlines
    text = text.replace("\n", " ")

    text = text.strip()

    return text


# ==========================================
# SENTIMENT ANALYSIS FUNCTION
# ==========================================

def analyze_sentiment(text):

    # Load model only once
    load_model()

    # Clean text
    text = clean_text(text)

    # Skip empty comments
    if len(text) == 0:

        return "NEUTRAL", 0.0

    # Limit text length
    text = text[:512]

    # Run sentiment analysis
    result = classifier(text)[0]

    label = result["label"]

    score = float(result["score"])

    return label, score