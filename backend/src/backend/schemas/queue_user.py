from pydantic import BaseModel


class QueueUserResponse(BaseModel):
    username: str
    position: int


class QueueResponse(BaseModel):
    room_code: str
    users: list[QueueUserResponse]