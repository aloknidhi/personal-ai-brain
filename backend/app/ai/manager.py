"""AI Manager - coordinates all AI components."""

from sqlalchemy.orm import Session
from app.models.user import User
from app.ai.topic_extractor import TopicExtractor
from app.ai.knowledge_assessor import KnowledgeAssessor
from app.ai.planner import StudyPlanner
from typing import Dict, Any, List, Optional
from datetime import datetime


class AIManager:
    """Coordinate topic extraction, knowledge assessment, and planning."""

    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def analyze_conversations(self, conversation_ids: List[str]) -> Dict[str, Any]:
        """Run full AI analysis pipeline on conversations."""
        # Step 1: Extract topics
        extractor = TopicExtractor(self.db, self.current_user)
        extraction_result = extractor.extract_from_conversations(conversation_ids)

        # Step 2: Assess knowledge
        assessor = KnowledgeAssessor(self.db, self.current_user)
        assessment = assessor.assess_knowledge(conversation_ids)

        return {
            "extraction": extraction_result,
            "assessment": assessment,
        }

    def create_study_plan(
        self,
        title: str,
        goal: str,
        topics: List[str],
        daily_hours: int,
        days: int,
        start_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Create a personalized study plan."""
        planner = StudyPlanner(self.db, self.current_user)
        return planner.generate_plan(title, goal, topics, daily_hours, days, start_date)
