from pydantic import BaseModel


class QueueUserResponse(BaseModel):
    username: str
    position: int