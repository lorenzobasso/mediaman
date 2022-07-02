from enum import Enum
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Session, select


class Status(Enum):
    old = "old"
    new = "new"
    ignored = "ignored"
    liked = "liked"


class Video(SQLModel, table=True):
    id: str = Field(primary_key=True)
    channel_id: str
    title: str
    description: str
    published: str
    status: str = Field(default=Status.old.value)

    thumbnails: List["VideoThumbnail"] = Relationship(back_populates="video")


class VideoThumbnail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    size: str
    url: str
    height: int
    width: int

    video_id: str = Field(foreign_key="video.id")
    video: Video = Relationship(back_populates="thumbnails")


def parse_thumbnail(size, thumbnail) -> VideoThumbnail:
    return VideoThumbnail(
        size=size,
        url=thumbnail["url"],
        height=thumbnail["height"],
        width=thumbnail["width"],
    )


def parse_thumbnails(thumbnails) -> List[VideoThumbnail]:
    return [parse_thumbnail(size, t) for size, t in thumbnails.items()]


def parse(video, status=Status.old.value) -> Video:
    snippet = video["snippet"]

    return Video(
        id=snippet["resourceId"]["videoId"],
        channel_id=snippet["channelId"],
        title=snippet["title"],
        description=snippet["description"],
        published=snippet["publishedAt"],
        status=status,
        thumbnails=parse_thumbnails(snippet["thumbnails"]),
    )


def get_ids(db: Session, channel_id: str) -> List[str]:
    query = select(Video.id).where(Video.channel_id == channel_id)
    return db.exec(query).all()


def put_all(db: Session, videos: List[Video]):
    channels = {v.channel_id for v in videos}
    ids = []

    for channel in channels:
        ids.extend(get_ids(db, channel))

    videos = [v for v in videos if v.id not in ids]

    db.add_all(videos)
    db.commit()
