from pydantic import BaseModel
from typing import List, Optional
import datetime
import uuid


class UserSchemaBase(BaseModel):
    username: str
    first_name: str
    last_name: str


class UserSchemaInDB(UserSchemaBase):
    class Config:
        from_attributes = True


class UserSchemaCreate(UserSchemaBase):
    pass


class UserSchema(UserSchemaInDB):
    meetings: Optional[List["MeetingSchemaInDB"]] = None


class MeetingSchemaBase(BaseModel):
    title: str
    user_id: Optional[str] = None
    description: str | None = None
    start_date: datetime.datetime
    end_date: datetime.datetime


class MeetingSchemaCreate(MeetingSchemaBase):
    pass


class MeetingSchemaInDB(MeetingSchemaBase):
    id: uuid.UUID
    user_id: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class MeetingSchema(MeetingSchemaInDB):
    users: Optional[List["UserSchemaInDB"]] = None
