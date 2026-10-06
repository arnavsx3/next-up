# ruff: noqa: B008

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...schemas.queue import QueueResponse
from ...schemas.queue_user import QueueListResponse, QueueUserResponse
from ...services.queue_service import (
    create_queue,
    get_queue_users,
    join_queue,
)

router = APIRouter(prefix="/queues", tags=["queues"])


@router.post("/", response_model=QueueResponse)
def create_new_queue(db: Session = Depends(get_db)):
    return create_queue(db)


@router.post("/{room_code}/join", response_model=QueueUserResponse)
def join_existing_queue(
    room_code: str,
    db: Session = Depends(get_db),
):
    user = join_queue(db, room_code)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Queue not found",
        )

    position = (
        db.query(type(user))
        .filter(type(user).queue_id == user.queue_id)
        .filter(type(user).id <= user.id)
        .count()
    )

    return {
        "username": user.username,
        "position": position,
    }


@router.get("/{room_code}", response_model=QueueListResponse)
def get_queue(
    room_code: str,
    db: Session = Depends(get_db),
):
    users = get_queue_users(db, room_code)

    if users is None:
        raise HTTPException(
            status_code=404,
            detail="Queue not found",
        )

    return {
        "room_code": room_code,
        "users": users,
    }