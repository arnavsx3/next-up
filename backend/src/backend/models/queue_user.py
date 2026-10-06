from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class QueueUser(Base):
    __tablename__ = "queue_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)

    queue_id: Mapped[int] = mapped_column(
        ForeignKey("queues.id"),
        nullable=False,
    )

    queue = relationship("Queue", back_populates="users")