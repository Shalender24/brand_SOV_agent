import pandas as pd
import re
import os
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import json
from config import SEARCH_QUERY

# Download required nltk data (only run once)
nltk.download("punkt")
nltk.download("stopwords")
nltk.download('punkt_tab')

def clean_text(text, brand_name):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # remove punctuation/numbers
    text = text.replace(brand_name.lower(), "")  # remove brand name itself
    return text

def extract_keywords(comments, brand_name, top_n=15):
    stop_words = set(stopwords.words("english"))
    words = []
    
    for comment in comments:
        cleaned = clean_text(comment, brand_name)
        tokens = word_tokenize(cleaned)
        filtered = [w for w in tokens if w not in stop_words and len(w) > 2]
        words.extend(filtered)
    
    return Counter(words).most_common(top_n)

def analyze_comments(csv_files, brand_name):
    if isinstance(csv_files, str):
        csv_files = [csv_files]

    dfs = [pd.read_csv(f) for f in csv_files]
    df = pd.concat(dfs, ignore_index=True)

    # Ensure sentiment column exists (score -1,0,1)
    if "sentiment_score" not in df.columns:
        raise ValueError("CSV must include sentiment_score column (-1,0,1)")

    # Filter comments mentioning brand
    df = df[df["comment_text"].str.lower().str.contains(brand_name.lower(), na=False)]

    # Separate positive and negative
    pos_comments = df[df["sentiment_score"] > 0]["comment_text"].tolist()
    neg_comments = df[df["sentiment_score"] < 0]["comment_text"].tolist()

    pos_keywords = extract_keywords(pos_comments, brand_name)
    neg_keywords = extract_keywords(neg_comments, brand_name)

    return {
        "positive_keywords": pos_keywords,
        "negative_keywords": neg_keywords
    }


def save_json(data, filepath):
    """Save Python dict/list as JSON"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
        
def run_analyze():
    comments=[]
    for query in SEARCH_QUERY:
        query=query.replace(" ","-")
        query_path=f"data/{query}_comments.csv"
        comments.append(query_path)
    
    results=analyze_comments(comments,brand_name='atomberg')
    save_json(results, "data/final_keywords.json")
    print("\n📁 Results saved to data/final_keywords.json")

if __name__ == "__main__":
    
    comments=[]
    for query in SEARCH_QUERY:
        query=query.replace(" ","-")
        query_path=f"data/{query}_comments.csv"
        comments.append(query_path)
    
    results=analyze_comments(comments,brand_name='atomberg')

    print("\n🌟 Positive keywords:")
    for word, freq in results["positive_keywords"]:
        print(f"{word} ({freq})")

    print("\n⚠️ Negative keywords:")
    for word, freq in results["negative_keywords"]:
        print(f"{word} ({freq})")
        
    save_json(results, "data/final_analysis.json")
    print("\n📁 Results saved to data/final_analysis.json")

