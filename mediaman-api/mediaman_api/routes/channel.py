from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from mediaman_api.youtube import yt_session, get_channel_info
from mediaman_api.models import channel
from mediaman_api.database import db_session

router = APIRouter()


@router.post("/search-channel", response_model=channel.Channel)
def search_youtube_channel_by_id(
    id: str = "UCtKUW8LJK2Ev8hUy9ZG_PPA",
    yt=Depends(yt_session),
    db: Session = Depends(db_session),
):
    if not id:
        raise HTTPException(status_code=400, detail="You need to specify a channel id")

    try:
        info = get_channel_info(id, yt)
        new_channel = channel.parse(info)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"No channel with id={id}")

    db_channel = channel.patch(db, new_channel)

    return db_channel
