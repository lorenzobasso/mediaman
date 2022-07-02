from typing import Dict, List, Optional
from sqlmodel import SQLModel, Field, Relationship, Session


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


def parse_thumbnail(size, thumbnail) -> ChannelThumbnail:
    return ChannelThumbnail(
        size=size,
        url=thumbnail["url"],
        height=thumbnail["height"],
        width=thumbnail["width"],
    )


def parse_thumbnails(thumbnails) -> List[ChannelThumbnail]:
    return [parse_thumbnail(size, t) for size, t in thumbnails.items()]


def parse(channel) -> Channel:
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


def get(db: Session, id: str):
    return db.get(Channel, id)


def put(db: Session, channel: Channel):
    db.add(channel)
    db.refresh(channel)
    db.commit()

    return channel


def patch(db: Session, new_data: Channel):
    db_channel = get(db, new_data.id)

    if db_channel is None:
        db_channel = new_data
    else:
        new_data_dict = new_data.dict(exclude_defaults=True)
        for attr, val in new_data_dict.items():
            print(attr)
            setattr(db_channel, attr, val)

    return put(db, db_channel)
