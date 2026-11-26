"""Study Planner API endpoints with AI integration."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, StudyPlan, Task
from app.security import get_current_user
from app.schemas import StudyPlanCreate, StudyPlanOut, TaskCreate, TaskOut
from app.ai.manager import AIManager
from datetime import datetime

router = APIRouter()


@router.post("/generate", response_model=dict)
def generate_plan(
    plan_in: StudyPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate an AI-powered study plan."""
    ai_manager = AIManager(db, current_user)
    result = ai_manager.create_study_plan(
        title=plan_in.title,
        goal=plan_in.title,
        topics=[],  # Will be filled from knowledge base
        daily_hours=4,
        days=30,
        start_date=plan_in.start_date,
    )
    return result


@router.post("/generate-detailed", response_model=dict)
def generate_plan_detailed(
    title: str = Query(...),
    goal: str = Query(...),
    topics: list[str] = Query([]),
    daily_hours: int = Query(4),
    days: int = Query(30),
    start_date: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate a detailed study plan with specific parameters."""
    sd = datetime.fromisoformat(start_date) if start_date else None
    ai_manager = AIManager(db, current_user)
    result = ai_manager.create_study_plan(
        title=title,
        goal=goal,
        topics=topics,
        daily_hours=daily_hours,
        days=days,
        start_date=sd,
    )
    return result


@router.get("/", response_model=list[StudyPlanOut])
def list_plans(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(StudyPlan).filter(StudyPlan.user_id == current_user.id).all()


@router.get("/{plan_id}", response_model=StudyPlanOut)
def get_plan(plan_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(StudyPlan).filter(StudyPlan.id == plan_id, StudyPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.post("/{plan_id}/tasks", response_model=TaskOut)
def add_task(plan_id: str, task_in: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(StudyPlan).filter(StudyPlan.id == plan_id, StudyPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    task = Task(plan_id=plan_id, topic_id=task_in.topic_id, title=task_in.title, deadline=task_in.deadline)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: str, status: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).join(StudyPlan).filter(Task.id == task_id, StudyPlan.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = status
    db.commit()
    db.refresh(task)
    return task
