from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, Activity
from app.security import get_current_user
from app.schemas import ActivityStart, ActivityOut
from datetime import datetime

router = APIRouter()


@router.post("/start", response_model=ActivityOut)
def start_activity(activity_in: ActivityStart, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    activity = Activity(
        user_id=current_user.id,
        task_id=activity_in.task_id,
        title=activity_in.title,
        started_at=datetime.utcnow(),
        status="in_progress",
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@router.post("/{activity_id}/stop", response_model=ActivityOut)
def stop_activity(activity_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id, Activity.user_id == current_user.id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity.ended_at = datetime.utcnow()
    activity.status = "completed"
    db.commit()
    db.refresh(activity)
    return activity


@router.get("/", response_model=list[ActivityOut])
def list_activities(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Activity).filter(Activity.user_id == current_user.id).order_by(Activity.started_at.desc()).all()
