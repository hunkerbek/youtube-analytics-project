import json
from src.youtube_object import YoutubeObject

# import isodate

class Channel(YoutubeObject):
    """Класс для ютуб-канала"""


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__response = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other):
        return self.subscriberCount - other.subscriberCount

    def __eq__(self, other):
        return self.subscriberCount == other.subscriberCount

    def __gt__(self, other):
        return self.subscriberCount > other.subscriberCount

    def __ge__(self, other):
        return self.subscriberCount >= other.subscriberCount

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__response["items"][0]["snippet"]["title"]

    @property
    def description(self):
        return self.__response["items"][0]["snippet"]["description"]

    @property
    def video_count(self):
        return int(self.__response["items"][0]["statistics"]["videoCount"])

    @property
    def viewCount(self):
        return int(self.__response["items"][0]["statistics"]["viewCount"])

    @property
    def url(self):
        return f"https://www.youtube.com/channel/{self.__channel_id}"

    @property
    def subscriberCount(self):
        return int(self.__response["items"][0]["statistics"]["subscriberCount"])

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(self.__response)

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump({"id": self.__channel_id, "title": self.title, "description": self.description,
                       "video_count": self.video_count, "viewCount": self.viewCount, "url": self.url,
                       "subscriberCount": self.subscriberCount}, file, ensure_ascii=False)
