"""Analysis API endpoints with real AI integration."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, Conversation, Analysis
from app.security import get_current_user
from app.schemas import AnalysisCreate, AnalysisOut
from app.ai.manager import AIManager

router = APIRouter()


@router.post("/preview", response_model=AnalysisOut)
def preview_analysis(analysis_in: AnalysisCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Run AI analysis on a conversation (preview mode)."""
    if analysis_in.conversation_id:
        conv = db.query(Conversation).filter(
            Conversation.id == analysis_in.conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")

    ai_manager = AIManager(db, current_user)
    result = ai_manager.analyze_conversations([analysis_in.conversation_id] if analysis_in.conversation_id else [])

    analysis = Analysis(
        user_id=current_user.id,
        conversation_id=analysis_in.conversation_id,
        analysis_type=analysis_in.analysis_type,
        result=str(result),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.post("/analyze-selected")
def analyze_selected(
    conversation_ids: list[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Run AI analysis on multiple selected conversations."""
    # Verify all conversations belong to user
    for conv_id in conversation_ids:
        conv = db.query(Conversation).filter(
            Conversation.id == conv_id,
            Conversation.user_id == current_user.id
        ).first()
        if not conv:
            raise HTTPException(status_code=404, detail=f"Conversation {conv_id} not found")

    ai_manager = AIManager(db, current_user)
    result = ai_manager.analyze_conversations(conversation_ids)

    # Save analysis
    analysis = Analysis(
        user_id=current_user.id,
        analysis_type="bulk_analysis",
        result=str(result),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return {"analysis_id": analysis.id, "result": result}


@router.get("/", response_model=list[AnalysisOut])
def list_analyses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Analysis).filter(Analysis.user_id == current_user.id).all()
