import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str):
        self.video_id: str = video_id
        self.video_info: dict = self.get_video_info(video_id)
        self.video_title: str = self.video_info["items"][0]["snippet"]["title"]
        self.video_url: str = "https://www.youtube.com/watch?v=" + f"{video_id}"
        self.view_count: int = int(self.video_info["items"][0]["statistics"]["viewCount"])
        self.video_like_count: int = int(self.video_info["items"][0]["statistics"]["likeCount"])

    def __str__(self) -> str:
        return f"{self.video_title}"

    @classmethod
    def get_service(cls):
        """
        Метод возвращает объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @classmethod
    def get_video_info(cls, video_id: str) -> dict:
        """
        Метод возвращает информацию о видеоролике по его ID
        """
        video_response = cls.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id).execute()
        return video_response


class PLVideo:
    def __init__(self, video_id: str, playlist_id: str):
        self.video_id: str = video_id
        self.playlist_id: str = playlist_id
        self.playlist_info: dict = self.get_playlist_info(playlist_id)
        self.video_info: dict = self.get_video_info(video_id)
        self.video_title: str = self.video_info["items"][0]["snippet"]["title"]
        self.video_url: str = "https://www.youtube.com/watch?v=" + f"{video_id}"
        self.view_count: int = int(self.video_info["items"][0]["statistics"]["viewCount"])
        self.video_like_count: int = int(self.video_info["items"][0]["statistics"]["likeCount"])

    def __str__(self) -> str:
        return f"{self.video_title}"

    @classmethod
    def get_service(cls):
        """
        Метод возвращает объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @classmethod
    def get_playlist_info(cls, playlist_id: str) -> dict:
        """
        Метод возвращает информацию о видеоролике по его ID
        """
        playlist_response = cls.get_service().playlistItems().list(playlistId=playlist_id,
                                               part='contentDetails,snippet',
                                               maxResults=50,
                                               ).execute()
        return playlist_response

    def get_playlist_videos(self) -> list[str]:
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_info['items']]
        return video_ids

    def get_video_info(self, video_id: str) -> dict:
        if video_id in self.get_playlist_videos():
            video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id).execute()
        else:
            video_response = {}
        return video_response
