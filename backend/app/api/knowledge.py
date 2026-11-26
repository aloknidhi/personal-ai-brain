from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, Subject, Topic, KnowledgeRecord
from app.security import get_current_user
from app.schemas import SubjectCreate, SubjectOut, TopicCreate, TopicOut, KnowledgeRecordOut

router = APIRouter()


@router.get("/subjects", response_model=list[SubjectOut])
def list_subjects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Subject).filter(Subject.user_id == current_user.id).all()


@router.post("/subjects", response_model=SubjectOut)
def create_subject(subject_in: SubjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subject = Subject(user_id=current_user.id, name=subject_in.name)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.get("/topics", response_model=list[TopicOut])
def list_topics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Topic).join(Subject).filter(Subject.user_id == current_user.id).all()


@router.post("/topics", response_model=TopicOut)
def create_topic(topic_in: TopicCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Verify subject belongs to current user
    subject = db.query(Subject).filter(Subject.id == topic_in.subject_id, Subject.user_id == current_user.id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    topic = Topic(
        subject_id=topic_in.subject_id,
        parent_topic_id=topic_in.parent_topic_id,
        name=topic_in.name,
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


@router.get("/", response_model=list[KnowledgeRecordOut])
def get_knowledge(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(KnowledgeRecord).filter(KnowledgeRecord.user_id == current_user.id).all()
