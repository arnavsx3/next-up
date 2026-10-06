import random
import string

from sqlalchemy.orm import Session

from ..models.queue import Queue
from ..models.queue_user import QueueUser

ADJECTIVES = [
    "sleepy",
    "angry",
    "tiny",
    "lazy",
    "happy",
    "confused",
]

NOUNS = [
    "penguin",
    "toast",
    "potato",
    "pickle",
    "banana",
    "hamster",
]


def generate_username() -> str:
    return f"{random.choice(ADJECTIVES)}_{random.choice(NOUNS)}"


def generate_room_code() -> str:
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choices(characters, k=6))


def create_queue(db: Session) -> Queue:
    room_code = generate_room_code()

    queue = Queue(room_code=room_code)

    db.add(queue)
    db.commit()
    db.refresh(queue)

    return queue


def join_queue(db: Session, room_code: str) -> QueueUser | None:
    queue = (
        db.query(Queue)
        .filter(Queue.room_code == room_code)
        .first()
    )

    if not queue:
        return None

    user = QueueUser(
        username=generate_username(),
        queue_id=queue.id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_queue_users(db: Session, room_code: str):
    queue = (
        db.query(Queue)
        .filter(Queue.room_code == room_code)
        .first()
    )

    if not queue:
        return None

    users = (
        db.query(QueueUser)
        .filter(QueueUser.queue_id == queue.id)
        .order_by(QueueUser.id)
        .all()
    )

    return [
        {
            "username": user.username,
            "position": position,
        }
        for position, user in enumerate(users, start=1)
    ]

def leave_queue(db: Session, room_code: str, user_id: int) -> bool:
    queue = (
        db.query(Queue)
        .filter(Queue.room_code == room_code)
        .first()
    )

    if not queue:
        return False

    user = (
        db.query(QueueUser)
        .filter(
            QueueUser.id == user_id,
            QueueUser.queue_id == queue.id,
        )
        .first()
    )

    if not user:
        return False

    db.delete(user)
    db.commit()

    return True