"""ChatGPT import and source sync API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, DataSource, Conversation
from app.security import get_current_user
from app.importers.chatgpt_importer import ChatGPTImporter

router = APIRouter()


@router.post("/import/chatgpt")
def import_chatgpt(
    file: UploadFile = File(...),
    source_id: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Import a ChatGPT conversation export ZIP/JSON file."""
    # Verify source exists and belongs to user
    source = None
    if source_id:
        source = db.query(DataSource).filter(
            DataSource.id == source_id,
            DataSource.user_id == current_user.id
        ).first()
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")

    # Read file content
    content = file.file.read()

    # Import
    importer = ChatGPTImporter(db, current_user)
    effective_source_id = source_id or (source.id if source else None)
    if not effective_source_id:
        raise HTTPException(status_code=400, detail="Source ID is required")

    result = importer.import_zip(content, effective_source_id)
    return result


@router.post("/sources/{source_id}/sync")
def sync_source(
    source_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Sync a data source (re-import/check for new data)."""
    source = db.query(DataSource).filter(
        DataSource.id == source_id,
        DataSource.user_id == current_user.id
    ).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    from datetime import datetime
    source.last_sync = datetime.utcnow()
    db.commit()

    return {
        "source_id": source_id,
        "source_type": source.source_type,
        "status": "synced",
        "last_sync": source.last_sync.isoformat() if source.last_sync else None,
    }


@router.get("/sources/{source_id}/conversations")
def get_source_conversations(
    source_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all conversations for a specific source."""
    source = db.query(DataSource).filter(
        DataSource.id == source_id,
        DataSource.user_id == current_user.id
    ).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    conversations = db.query(Conversation).filter(
        Conversation.source_id == source_id,
        Conversation.user_id == current_user.id
    ).all()

    return [{"id": c.id, "title": c.title, "external_id": c.external_id} for c in conversations]
