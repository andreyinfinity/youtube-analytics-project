import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str):
        self.id: str = video_id
        self.__info: dict = self.get_video_info(video_id)
        try:
            self.title: str = self.__info["items"][0]["snippet"]["title"]
            self.url: str = "https://www.youtube.com/watch?v=" + f"{video_id}"
            self.view_count: int = int(self.__info["items"][0]["statistics"]["viewCount"])
            self.like_count: int = int(self.__info["items"][0]["statistics"]["likeCount"])
        except IndexError:
            self.title: str | None = None
            self.url: str | None = None
            self.view_count: int | None = None
            self.like_count: int | None = None

    def __str__(self) -> str:
        return f"{self.title}"

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


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
