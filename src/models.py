from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import DateTime


from typing import List, Optional
import uuid
import datetime


class Base(DeclarativeBase):
    pass


class UserMeetingLink(Base):
    __tablename__ = "user_meeting_link"
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.username", ondelete="CASCADE"), primary_key=True
    )
    meeting_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("meetings.id", ondelete="CASCADE"), primary_key=True
    )


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    meetings: Mapped[List["Meeting"]] = relationship(
        "Meeting", secondary="user_meeting_link", back_populates="users"
    )


class Meeting(Base):
    __tablename__ = "meetings"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.username", ondelete="CASCADE")
    )
    title: Mapped[str]
    description: Mapped[Optional[str]]
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    users: Mapped[List["User"]] = relationship(
        "User", secondary="user_meeting_link", back_populates="meetings"
    )
