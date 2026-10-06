from pydantic import BaseModel


class QueueCreate(BaseModel):
    pass


class QueueResponse(BaseModel):
    room_code: str