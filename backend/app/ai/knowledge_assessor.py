"""AI Knowledge Assessor - assesses user knowledge levels."""

from sqlalchemy.orm import Session
from app.models.user import User, KnowledgeRecord, Topic, Analysis
from typing import Dict, Any, List
from datetime import datetime


class KnowledgeAssessor:
    """Assess user knowledge based on conversation analysis and activities."""

    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def assess_knowledge(self, conversation_ids: List[str]) -> Dict[str, Any]:
        """Assess knowledge levels from analyzed conversations."""
        assessment = {
            "subjects": {},
            "overall_confidence": 0.0,
            "recommendations": [],
        }

        # Get all knowledge records for this user
        records = self.db.query(KnowledgeRecord).filter(
            KnowledgeRecord.user_id == self.current_user.id
        ).all()

        for record in records:
            topic = self.db.query(Topic).filter(Topic.id == record.topic_id).first()
            if not topic:
                continue
            subject = self.db.query(Topic).join(Topic.subject).filter(
                Topic.id == record.topic_id
            ).first()

            subj_name = "General"
            if topic and topic.subject:
                subj_name = topic.subject.name

            if subj_name not in assessment["subjects"]:
                assessment["subjects"][subj_name] = []

            assessment["subjects"][subj_name].append({
                "topic": topic.name if topic else "Unknown",
                "mastery_status": record.mastery_status,
                "confidence": record.confidence,
            })

        # Calculate overall confidence
        if records:
            confidences = [float(r.confidence) for r in records if r.confidence]
            if confidences:
                assessment["overall_confidence"] = sum(confidences) / len(confidences)

        # Generate recommendations
        weak_topics = self.db.query(KnowledgeRecord).join(Topic).filter(
            KnowledgeRecord.user_id == self.current_user.id,
            KnowledgeRecord.mastery_status.in_(["needs_practice", "needs_revision"]),
        ).all()

        for record in weak_topics:
            topic = self.db.query(Topic).filter(Topic.id == record.topic_id).first()
            if topic:
                assessment["recommendations"].append(
                    f"Review {topic.name} - marked as {record.mastery_status}"
                )

        # Save assessment
        analysis = Analysis(
            user_id=self.current_user.id,
            analysis_type="knowledge_assessment",
            result=str(assessment),
        )
        self.db.add(analysis)
        self.db.commit()

        return assessment
