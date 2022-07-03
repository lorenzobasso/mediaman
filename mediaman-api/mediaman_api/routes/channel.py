from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from mediaman_api import youtube
from mediaman_api.models import channel, video
from mediaman_api.database import db_session

router = APIRouter()


def check_channel_id(id: str) -> str:
    id = id.strip()
    if not id:
        raise HTTPException(status_code=400, detail="You need to specify a channel id")

    return id


def check_channel(db: Session, id: str) -> channel.Channel:
    db_channel = channel.get(db, id)
    if not db_channel:
        raise HTTPException(status_code=404, detail=f"No channel with id={id}")

    return db_channel


@router.put("/channel", response_model=channel.ChannelResponse)
def search_youtube_channel_by_id(
    id: str = "UCtKUW8LJK2Ev8hUy9ZG_PPA",
    yt=Depends(youtube.yt_session),
    db: Session = Depends(db_session),
):
    id = check_channel_id(id)

    try:
        info = youtube.get_channel_info(id, yt)
        new_channel = channel.parse(info)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"No channel with id={id}")

    db_channel = channel.patch(db, new_channel)

    return channel.parse_response(db_channel)


@router.patch("/follow-channel", response_model=bool)
def search_youtube_channel_by_id(
    id: str = "UCtKUW8LJK2Ev8hUy9ZG_PPA", db: Session = Depends(db_session)
):
    id = check_channel_id(id)
    db_channel = check_channel(db, id)

    db_channel.following = not db_channel.following

    channel.put(db, db_channel)

    return db_channel.following


@router.put("/library")
def add_channel_library(
    id: str = "UCtKUW8LJK2Ev8hUy9ZG_PPA",
    yt=Depends(youtube.yt_session),
    db: Session = Depends(db_session),
):
    id = check_channel_id(id)
    db_channel = check_channel(db, id)

    library = youtube.get_channel_library(yt, db_channel.uploadPlaylist)
    videos = [video.parse(v) for v in library]

    video.put_all(db, videos)

    return len(videos)


@router.patch("/library")
def update_channel_library(
    id: str = "UCtKUW8LJK2Ev8hUy9ZG_PPA",
    yt=Depends(youtube.yt_session),
    db: Session = Depends(db_session),
):
    id = check_channel_id(id)
    db_channel = check_channel(db, id)

    old_ids = video.get_ids(db, id)
    new_videos = youtube.check_for_updates(yt, db_channel.uploadPlaylist, old_ids)
    new_videos = [video.parse(v, video.Status.new.value) for v in new_videos]

    video.put_all(db, new_videos)

    return len(new_videos)


@router.get("/channels", response_model=List[channel.ChannelResponse])
def get_followed_channels(db: Session = Depends(db_session)):
    channels = channel.get_followed(db)

    return [channel.parse_response(ch) for ch in channels]
