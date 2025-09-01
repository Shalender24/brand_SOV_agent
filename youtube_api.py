# youtube_api.py
from googleapiclient.discovery import build
import pandas as pd
from config import YOUTUBE_API_KEY, SEARCH_QUERY, MAX_RESULTS, BRANDS

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_videos(QUERY):
    request = youtube.search().list(
        q=QUERY,
        part="id,snippet",
        maxResults=MAX_RESULTS,
        type="video"
    )
    response = request.execute()
    return response.get("items", [])

def get_video_details(video_ids):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )
    response = request.execute()
    return response.get("items", [])

def get_comments(video_id, max_results=100):
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response.get("items", []):
            top_comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "video_id": video_id,
                "comment_id": item["id"],
                "author": top_comment.get("authorDisplayName"),
                "comment_text": top_comment.get("textDisplay"),
                "likes": top_comment.get("likeCount"),
                "published_date": top_comment.get("publishedAt")
            })
        
    except Exception as e:
        print(f"⚠️ Error fetching comments for {video_id}: {e}")
    return comments
