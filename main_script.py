# main.py
from youtube_api import search_videos, get_video_details, get_comments
from sentiment import analyze_sentiment
from utils import save_csv, detect_brands
from config import BRANDS, SEARCH_QUERY
import os

def main():
    os.makedirs("data", exist_ok=True)
    
    for query in SEARCH_QUERY:

        # Step 1: Search videos
        query=query.replace(" ","-")
        videos = search_videos(query)
        video_ids = [v["id"]["videoId"] for v in videos]

        # Step 2: Fetch video details
        video_data = []
        for vid in get_video_details(video_ids):
            snippet = vid["snippet"]
            stats = vid["statistics"]

            brand_mentions = detect_brands(snippet["title"] + " " + snippet.get("description", ""))
            video_data.append({
                "video_id": vid["id"],
                "title": snippet["title"],
                "channel_name": snippet["channelTitle"],
                "published_date": snippet["publishedAt"],
                "views": stats.get("viewCount"),
                "likes": stats.get("likeCount"),
                "comment_count": stats.get("commentCount"),
                "video_url": f"https://youtube.com/watch?v={vid['id']}",
                **brand_mentions
            })

        save_csv(video_data, f"data/{query}_videos.csv")

        # Step 3: Fetch comments & sentiment
        comments_data = []
        for vid in video_ids:
            comments = get_comments(vid)
            for c in comments:
                brand_mentions = detect_brands(c["comment_text"])
                sentiment, score = analyze_sentiment(c["comment_text"])
                comments_data.append({
                    **c,
                    **brand_mentions,
                    "sentiment": sentiment,
                    "sentiment_score": score
                })

        save_csv(comments_data, f"data/{query}_comments.csv")

if __name__ == "__main__":
    main()
