from src.youtube_object import YoutubeObject


class Video(YoutubeObject):

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id
        self.__response = Video.youtube.videos().list(part='snippet,statistics',
                                                      id=video_id
                                                      ).execute()

    def __str__(self):
        return self.title

    @property
    def video_id(self):
        return self.__video_id

    @property
    def title(self):
        return self.__response["items"][0]["snippet"]["title"]

    @property
    def url(self):
        return f"https://youtu.be/{self.__video_id}"

    @property
    def viewCount(self):
        return int(self.__response["items"][0]["statistics"]["viewCount"])

    @property
    def likeCount(self):
        return int(self.__response["items"][0]["statistics"]["likeCount"])


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        response = Video.youtube.playlistItems().list(part="id",
                                               playlistId=playlist_id,
                                               videoId=video_id
                                               ).execute()

        if int(response["pageInfo"]["totalResults"])   == 1:
            super().__init__(video_id)

        else:
            raise Exception("Видео нет в плейлисте")
