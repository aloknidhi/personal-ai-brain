from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, DataSource
from app.security import get_current_user
from app.schemas import DataSourceCreate, DataSourceOut
import uuid

router = APIRouter()


@router.post("/", response_model=DataSourceOut)
def connect_source(source_in: DataSourceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    source = DataSource(
        user_id=current_user.id,
        source_type=source_in.source_type,
        status="pending_approval",
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.get("/", response_model=list[DataSourceOut])
def list_sources(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(DataSource).filter(DataSource.user_id == current_user.id).all()


@router.delete("/{source_id}")
def delete_source(source_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    source = db.query(DataSource).filter(DataSource.id == source_id, DataSource.user_id == current_user.id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(source)
    db.commit()
    return {"message": "Source disconnected"}
