from pydantic import BaseModel


class QueueResponse(BaseModel):
    room_code: str