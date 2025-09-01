import pandas as pd
from config import SEARCH_QUERY
# Define target brands
BRANDS = ["atomberg", "havells", "orient", "crompton"]

def load_data(videos_path="data/videos.csv", comments_path="data/comments.csv"):
    videos = pd.read_csv(videos_path)
    comments = pd.read_csv(comments_path)
    return videos, comments

def count_mentions(text, brand):
    if pd.isna(text): 
        return 0
    return text.lower().count(brand.lower())

def compute_mentions(videos, comments):
    mention_counts = {brand: 0 for brand in BRANDS}
    
    # Mentions in videos
    for _, row in videos.iterrows():
        for brand in BRANDS:
            mention_counts[brand] += count_mentions(row.get("title", ""), brand)
            mention_counts[brand] += count_mentions(row.get("description", ""), brand)
    
    # Mentions in comments
    for _, row in comments.iterrows():
        for brand in BRANDS:
            mention_counts[brand] += count_mentions(row.get("comment_text", ""), brand)
    
    total = sum(mention_counts.values())
    mention_share = {b: mention_counts[b]/total if total>0 else 0 for b in BRANDS}
    return mention_share

def compute_engagement(videos):
    engagement = {brand: 0 for brand in BRANDS}
    
    for _, row in videos.iterrows():
        brand_found = None
        title_desc = f"{row.get('title','')} {row.get('description','')}".lower()
        for brand in BRANDS:
            if brand in title_desc:
                brand_found = brand
                break
        if brand_found:
            eng = row.get("views",0) + row.get("likes",0) + row.get("comments_count",0)
            engagement[brand_found] += eng
    
    total = sum(engagement.values())
    engagement_share = {b: engagement[b]/total if total>0 else 0 for b in BRANDS}
    return engagement_share

def compute_positive_voice(comments):
    positive_voice = {brand: 0 for brand in BRANDS}
    
    for _, row in comments.iterrows():
        if row.get("sentiment","").lower() == "positive":
            for brand in BRANDS:
                if brand in str(row.get("comment_text","")).lower():
                    positive_voice[brand] += 1
    
    total = sum(positive_voice.values())
    sovp = {b: positive_voice[b]/total if total>0 else 0 for b in BRANDS}
    return sovp

def compute_overall_sov(videos, comments, w_mentions=0.4, w_engagement=0.3, w_positive=0.3):
    mention_share = compute_mentions(videos, comments)
    engagement_share = compute_engagement(videos)
    positive_share = compute_positive_voice(comments)
    
    overall = {}
    for b in BRANDS:
        overall[b] = (
            w_mentions * mention_share[b] +
            w_engagement * engagement_share[b] +
            w_positive * positive_share[b]
        )
    
    return {
        "mention_share": mention_share,
        "engagement_share": engagement_share,
        "positive_share": positive_share,
        "overall_sov": overall
    }
    
def run_sov():
    with open("data/sov_summary.txt",'w') as f:
        for query in SEARCH_QUERY:
            query=query.replace(" ","-")
            video_path=f"data/{query}_videos.csv"
            comment_path=f"data/{query}_comments.csv"
            
            videos, comments = load_data(video_path,comment_path)
            results = compute_overall_sov(videos, comments)
            print("=== Share of Voice Results ===")
            f.write(f"\n stats for {query}:\n")
            for metric, values in results.items():
                print(f"\n{metric.upper()}:")
                f.write(f"\n{metric.upper()}:")
                for brand, score in values.items():
                    print(f"{brand}: {score:.2f}\n")
                    f.write(f"{brand}: {score:.2f}\n")

if __name__ == "__main__":
    run_sov()
    

                    
