from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...schemas.queue import QueueResponse
from ...schemas.queue_user import QueueUserResponse
from ...services.queue_service import create_queue, join_queue

router = APIRouter(prefix="/queues", tags=["queues"])


@router.post("/", response_model=QueueResponse)
def create_new_queue(db: Session = Depends(get_db)):
    queue = create_queue(db)
    return queue


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