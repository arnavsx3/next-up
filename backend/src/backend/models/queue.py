from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base

class Queue(Base):
    __tablename__ = "queues"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)

    users = relationship(
        "QueueUser",
        back_populates="queue",
        cascade="all, delete-orphan",
    )