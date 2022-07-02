from typing import List
import googleapiclient.discovery

from mediaman_api.utils import load_json

secrets_file = "secrets.json"
channel_parts = [
    "brandingSettings",
    "contentDetails",
    "contentOwnerDetails",
    "id",
    "localizations",
    "snippet",
    "statistics",
    "status",
    "topicDetails",
]
playlist_parts = [
    "contentDetails",
    "id",
    "snippet",
    "status",
]


def get_api_key():
    return load_json(secrets_file)["ytApiKey"]


def yt_session() -> googleapiclient.discovery.Resource:
    api = "youtube"
    version = "v3"

    return googleapiclient.discovery.build(
        api,
        version,
        developerKey=get_api_key(),
    )


def get_channel_info(id: str, yt: googleapiclient.discovery.Resource):
    request = yt.channels().list(
        part=",".join(channel_parts),
        id=id,
        maxResults=50,
    )
    response = request.execute()
    (channel,) = response["items"]

    return channel


def get_library_page(yt, uploadsId, pageToken):
    request = yt.playlistItems().list(
        part=",".join(playlist_parts),
        playlistId=uploadsId,
        maxResults=50,
        pageToken=pageToken,
    )

    response = request.execute()
    next_page = response.get("nextPageToken", None)
    videos = response["items"]

    return next_page, videos


def check_for_updates(
    yt: googleapiclient.discovery.Resource, uploads_id: str, old_ids: List[str]
):
    page_token = ""
    videos = []

    while page_token is not None:
        page_token, page = get_library_page(yt, uploads_id, page_token)
        new_videos = [
            v for v in page if v["snippet"]["resourceId"]["videoId"] not in old_ids
        ]
        videos.extend(new_videos)

        if len(new_videos) != len(page):
            page_token = None

    return videos


def get_channel_library(yt: googleapiclient.discovery.Resource, uploads_id: str):
    return check_for_updates(yt, uploads_id, [])
