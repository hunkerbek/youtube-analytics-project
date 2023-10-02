from datetime import timedelta
import isodate

from src.video import PLVideo, Video
from src.youtube_object import YoutubeObject
from operator import attrgetter


class PlayList(YoutubeObject):
    playlist_url = f'{YoutubeObject.base_url}/playlist'

    def __init__(self, playlist_id):
        super().__init__()

        self._playlist_id = playlist_id
        self._playlist_videos = None

        self.__response = self.youtube.playlists().list(
            id=self._playlist_id,
            part='snippet').execute()




    def __str__(self):
        return self.title

    @property
    def playlist_id(self):
        return self._playlist_id

    @property
    def title(self):
        return self.__response["items"][0]["snippet"]["title"]

    @property
    def url(self):
        """ video url """
        return f'https://www.youtube.com/playlist?list={self._playlist_id}'



    @property
    def total_duration(self) -> timedelta:
        """ playlist duration """
        playlist_videos = self.youtube.playlistItems().list(playlistId=self._playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        # printj(video_response)
        total_duration = timedelta(seconds=0)
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self) -> str | None:
        """ returns url for best video """

        playlist_videos = self.youtube.playlistItems().list(playlistId=self._playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        max_like_count = 0
        best_video_id = None
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like_count:
                max_like_count = like_count
                best_video_id = video['id']
        if best_video_id:
            return Video(best_video_id).url
        return None