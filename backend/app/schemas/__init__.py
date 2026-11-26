from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# Auth schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Data source schemas
class DataSourceCreate(BaseModel):
    source_type: str


class DataSourceOut(BaseModel):
    id: str
    source_type: str
    status: str
    last_sync: Optional[datetime] = None
    imported_count: int

    class Config:
        from_attributes = True


# Subject schemas
class SubjectCreate(BaseModel):
    name: str


class SubjectOut(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


# Topic schemas
class TopicCreate(BaseModel):
    name: str
    subject_id: str
    parent_topic_id: Optional[str] = None


class TopicOut(BaseModel):
    id: str
    name: str
    parent_topic_id: Optional[str] = None

    class Config:
        from_attributes = True


# Knowledge record schemas
class KnowledgeRecordOut(BaseModel):
    id: str
    topic_id: Optional[str] = None
    mastery_status: str
    confidence: str
    source_reference: Optional[str] = None

    class Config:
        from_attributes = True


# Conversation schemas
class ConversationOut(BaseModel):
    id: str
    title: Optional[str] = None
    external_id: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessageOut(BaseModel):
    id: str
    role: str
    content: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Study plan schemas
class StudyPlanCreate(BaseModel):
    title: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class StudyPlanOut(BaseModel):
    id: str
    title: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tasks: List["TaskOut"] = []

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    topic_id: Optional[str] = None
    deadline: Optional[datetime] = None


class TaskOut(BaseModel):
    id: str
    title: str
    status: str
    deadline: Optional[datetime] = None

    class Config:
        from_attributes = True


# Activity schemas
class ActivityStart(BaseModel):
    title: str
    task_id: Optional[str] = None


class ActivityOut(BaseModel):
    id: str
    title: str
    status: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Analysis schemas
class AnalysisCreate(BaseModel):
    conversation_id: Optional[str] = None
    analysis_type: str


class AnalysisOut(BaseModel):
    id: str
    analysis_type: str
    result: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


StudyPlanOut.model_rebuild()


class TokenData:
    def __init__(self, email: str | None = None):
        self.email = email
