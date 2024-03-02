from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from src.models import User, Meeting
from src.schemas import (
    MeetingSchemaCreate,
    MeetingSchema,
    UserSchema,
    UserSchemaCreate,
    MeetingSchemaInDB,
    UserSchemaInDB,
)
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import select
from src.database import get_session
from typing import List
import uuid

router = APIRouter()


@router.post("/users/{username}/meetings", response_model=MeetingSchema)
def create_meeting(
    username: str, meeting: MeetingSchemaCreate, session: Session = Depends(get_session)
):
    user = session.get(User, username)
    if user is None:
        raise HTTPException(
            status_code=400, detail=f"User with this '{username}' does not exist"
        )

    meeting.user_id = username
    meeting: Meeting = Meeting(**meeting.model_dump())
    meeting.users.append(user)
    session.add(meeting)
    session.commit()
    session.refresh(meeting)
    return meeting


@router.post("/users", response_model=UserSchema)
def create_user(user: UserSchemaCreate, session: Session = Depends(get_session)):
    user: User = User(**user.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/users", response_model=List[UserSchema])
def get_users(session: Session = Depends(get_session)):
    users = session.execute(select(User))
    return users.scalars().all()


@router.get("/meetings", response_model=List[MeetingSchema])
def get_meetings(session: Session = Depends(get_session)):
    meetings = session.execute(select(Meeting))
    return meetings.scalars().all()


@router.put("/meetings/{meeting_id}", response_model=MeetingSchema)
def add_user_to_meeting(
    meeting_id: uuid.UUID, username: str, session: Session = Depends(get_session)
):
    meeting = session.get(Meeting, meeting_id)
    if meeting is None:
        raise HTTPException(
            status_code=400,
            detail=f"The meeting with meeting_id:{meeting_id} does not exist",
        )

    user = session.get(User, username)
    if user is None:
        raise HTTPException(
            status_code=400, detail=f"User with this '{username}' does not exist"
        )

    for m in user.meetings:
        if meeting_id == m.id:
            raise HTTPException(
                status_code=400, detail="User is already registered in the meeting"
            )
        if not (m.start_date > meeting.end_date or m.end_date < meeting.start_date):
            raise HTTPException(
                status_code=400, detail=f"'{username}' has a meeting that overlaps"
            )

    meeting.users.append(user)
    session.add(meeting)
    session.commit()
    session.refresh(meeting)
    return meeting
