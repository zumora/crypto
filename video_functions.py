from datetime import datetime


def get_uploads_playlist_id(channel_id, youtube):
    # Retrieve the contentDetails part of the channel resource for the given channel ID
    channel_response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()

    # Extract the uploads playlist ID
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return uploads_playlist_id


def list_uploaded_videos(playlist_id, youtube):
    videos = []
    next_page_token = None

    # Retrieve videos in the playlist in pages (due to API response size limits)
    while True:
        playlistitems_response = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=50,  # Adjust the maxResults if necessary (max 50)
            pageToken=next_page_token
        ).execute()

        # Collect video IDs to query their statistics
        video_ids = [item['snippet']['resourceId']['videoId'] for item in playlistitems_response['items']]

        # Retrieve statistics for each video
        videos_response = youtube.videos().list(
            id=','.join(video_ids),
            part='snippet,statistics'
        ).execute()

        # Extract video information and statistics from each item
        for video in videos_response['items']:
            videos.append({
                'Title': video['snippet']['title'],
                'Video ID': video['id'],
                'Views': int(video['statistics']['viewCount']),
                'Published On': datetime.fromisoformat(video['snippet']['publishedAt'][:-1])
            })

        next_page_token = playlistitems_response.get('nextPageToken')
        if not next_page_token:
            break

    return videos