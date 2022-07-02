from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class Channel(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    description: str
    customUrl: str
    published: str
    country: str
    uploadPlaylist: str
    views: int
    subscribers: int
    videos: int
    banner: str
    following: bool = Field(default=False)

    thumbnails: List["ChannelThumbnail"] = Relationship(back_populates="channel")


class ChannelThumbnail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    size: str
    url: str
    height: int
    width: int

    channel_id: str = Field(foreign_key="channel.id")
    channel: Channel = Relationship(back_populates="thumbnails")


def parse_thumbnail(size, thumbnail):
    return ChannelThumbnail(
        size=size,
        url=thumbnail["url"],
        height=thumbnail["height"],
        width=thumbnail["width"],
    )


def parse_thumbnails(thumbnails):
    return [parse_thumbnail(size, t) for size, t in thumbnails.items()]


def parse(channel):
    snippet = channel["snippet"]
    stats = channel["statistics"]

    return Channel(
        id=channel["id"],
        title=snippet["title"],
        description=snippet["description"],
        customUrl=snippet["customUrl"],
        published=snippet["publishedAt"],
        country=snippet["country"],
        uploadPlaylist=channel["contentDetails"]["relatedPlaylists"]["uploads"],
        views=stats["viewCount"],
        subscribers=stats["subscriberCount"],
        videos=stats["videoCount"],
        banner=channel["brandingSettings"]["image"]["bannerExternalUrl"],
        thumbnails=parse_thumbnails(snippet["thumbnails"]),
    )
