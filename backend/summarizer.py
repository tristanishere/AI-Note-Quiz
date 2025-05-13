import sys
from transformers import pipeline
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

# load once
summarizer = pipeline("summarization", model="t5-base")
nlp = spacy.load("en_core_web_sm")

def summarize_text(text: str) -> str:
    # you can tweak max_length/min_length as needed
    result = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return result[0]["summary_text"]

def extract_keywords(text: str, top_n: int = 10):
    doc = nlp(text)
    chunks = [chunk.text for chunk in doc.noun_chunks]
    if not chunks:
        return []
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(chunks)
    scores = list(zip(tfidf.get_feature_names_out(), matrix.sum(axis=0).A1))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [word for word, _ in scores][:top_n]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python summarizer.py path/to/textfile.txt")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    print("Summary:\n", summarize_text(text))
    print("\nKeywords:", extract_keywords(text))

