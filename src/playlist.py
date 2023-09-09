import os
from googleapiclient.discovery import build
from isodate import parse_duration


class PlayList:
    def __init__(self, playlist_id: str):
        self.__id: str = playlist_id
        self.url: str = "https://www.youtube.com/playlist?list=" + f"{playlist_id}"
        self.title: str = self.__get_playlist_info()["items"][0]["snippet"]["title"]
        self.__properties = self.__get_video_properties()

    @classmethod
    def __get_service(cls):
        """
        Метод возвращает объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def __get_playlist_info(self) -> dict:
        """
        Метод API возвращает информацию о плейлисте по его ID.
        Используется для определения title плейлиста.
        """
        playlist_response = self.__get_service().playlists().list(id=self.__id,
                                               part='snippet',
                                               maxResults=50).execute()
        return playlist_response

    def __get_playlist_items(self) -> dict:
        """
        Метод API возвращает информацию о видеороликах плейлиста по его ID.
        Используется для поиска videoId в плейлисте.
        """
        playlist_response = self.__get_service().playlistItems().list(playlistId=self.__id,
                                               part='contentDetails',
                                               maxResults=50).execute()
        return playlist_response

    def __get_video_ids(self) -> list[str]:
        """
        Метод для парсинга и построения списка из videoId
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__get_playlist_items()['items']]
        return video_ids

    def __get_video_descriptions(self):
        """
        Метод API возвращает описание каждого видео.
        """
        videos_response = self.__get_service().videos().list(id=','.join(self.__get_video_ids()),
                                               part='contentDetails,statistics',
                                               maxResults=50).execute()
        return videos_response

    def __get_video_properties(self):
        """
        Метод для парсинга длительности видео и количества лайков видео.
        Возвращает список из словарей с ключами video_url, duration, view_count.
        """
        video_properties: list[dict] = []
        for video in self.__get_video_descriptions()['items']:
            properties_dict = {
                'video_url': 'https://youtu.be/' + video['id'],
                'duration': parse_duration(video['contentDetails']['duration']),
                'like_count': int(video['statistics']['likeCount']),
            }
            video_properties.append(properties_dict)
        return video_properties

    @property
    def total_duration(self):
        """Возвращает суммарную длительность всех видео из плейлиста."""
        total_duration = parse_duration('PT0S')
        for item in self.__properties:
            total_duration += item['duration']
        return total_duration

    def show_best_video(self):
        """
        Возвращает url видео из плейлиста с максимальным количеством лайков.
        """
        best_video = max(self.__properties, key=lambda elem: elem.get('like_count'))
        return best_video.get('video_url')


if __name__ == '__main__':
    pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
    # print(pl.get_video_descriptions())
    print(pl.total_duration)
    print(pl.show_best_video())
