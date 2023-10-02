from googleapiclient.discovery import build
import os
class YoutubeObject:

    base_url = None
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
