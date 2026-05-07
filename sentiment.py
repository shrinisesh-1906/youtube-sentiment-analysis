from transformers import pipeline

classifier = None

def load_model():
    global classifier

    if classifier is None:
        print("Loading sentiment model...")
        classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

def analyze_sentiment(text):
    load_model()

    text = str(text)[:512]

    result = classifier(text)[0]

    return result["label"], float(result["score"])