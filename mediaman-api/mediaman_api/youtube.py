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


def get_api_key():
    return load_json(secrets_file)["ytApiKey"]


def create_yt_session() -> googleapiclient.discovery.Resource:
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
