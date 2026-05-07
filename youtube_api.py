from googleapiclient.discovery import build
from config import API_KEY

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_id(query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="channel",
        maxResults=1
    )
    response = request.execute()
    
    return response['items'][0]['snippet']['channelId']


def get_uploads_playlist(channel_id):
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_videos(playlist_id):
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=10
    )
    response = request.execute()

    videos = []

    for item in response['items']:
        videos.append({
            "video_id": item['snippet']['resourceId']['videoId'],
            "title": item['snippet']['title']
        })

    return videos

def get_comments(video_id, max_comments=50):
    comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_comments, 100)
        )

        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']

            comments.append({
                "comment_id": item['id'],
                "text": comment['textDisplay'],
                "author": comment['authorDisplayName'],
                "likes": comment['likeCount']
            })

    except Exception as e:
        print(f"Error fetching comments for video {video_id}: {e}")

    return comments