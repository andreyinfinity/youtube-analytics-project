import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_info = self.get_channel_info(channel_id)
        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/' + self.channel_info['items'][0]['snippet']['customUrl']
        self.subscriber_count = self.channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_info['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_info['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Метод возвращает объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @classmethod
    def get_channel_info(cls, channel_id):
        """
        Метод возвращает информацию о канале по ID канала
        """
        channel_info = cls.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        return channel_info

    def to_json(self, filename):
        """
        Метод сохраняет атрибуты экземпляра класса в файл json.
        """
        file_content = {
            'channel_id': self.id,
            'channel_name': self.title,
            'channel_description': self.description,
            'channel_url': self.url,
            'channel_subscriber_count': self.subscriber_count,
            'channel_video_count': self.video_count,
            'channel_view_count': self.view_count,
            }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(file_content, file, ensure_ascii=False, indent=2)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        return print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))
