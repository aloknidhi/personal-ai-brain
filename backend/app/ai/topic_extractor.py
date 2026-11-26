"""AI Topic Extractor - extracts topics and concepts from conversations."""

from sqlalchemy.orm import Session
from app.models.user import User, Conversation, Message, Subject, Topic, KnowledgeRecord
from typing import List, Dict, Any
import re


class TopicExtractor:
    """Extract topics and concepts from conversations using lightweight NLP."""

    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def extract_from_conversations(self, conversation_ids: List[str]) -> Dict[str, Any]:
        """Extract topics from a list of conversations."""
        results = {
            "subjects_found": [],
            "topics_found": [],
            "conversations_analyzed": len(conversation_ids),
        }

        for conv_id in conversation_ids:
            conv = self.db.query(Conversation).filter(
                Conversation.id == conv_id,
                Conversation.user_id == self.current_user.id
            ).first()
            if not conv:
                continue

            messages = self.db.query(Message).filter(
                Message.conversation_id == conv_id
            ).order_by(Message.created_at).all()

            # Combine all message content
            full_text = " ".join([m.content for m in messages])

            # Extract potential topics using simple keyword detection
            topics = self._extract_topics_from_text(full_text, conv.title or "Untitled")

            for topic_name in topics:
                # Find or create subject
                subject = self._get_or_create_subject("General")
                # Find or create topic
                topic = self._get_or_create_topic(subject.id, topic_name)
                # Create knowledge record
                kr = KnowledgeRecord(
                    user_id=self.current_user.id,
                    topic_id=topic.id,
                    mastery_status="studied",
                    confidence="0.5",
                    source_reference=f"conversation:{conv_id}",
                )
                self.db.add(kr)

        self.db.commit()
        return results

    def _extract_topics_from_text(self, text: str, conversation_title: str) -> List[str]:
        """Extract topic keywords from text using simple heuristics."""
        topics = []
        # Common programming/learning keywords
        keywords = [
            'C++', 'Java', 'Python', 'JavaScript', 'TypeScript', 'React',
            'inheritance', 'polymorphism', 'constructor', 'operator overloading',
            'class', 'object', 'OOP', 'API', 'database', 'SQL', 'JDBC',
            'algorithm', 'data structure', 'function', 'variable', 'loop',
            'Japanese', 'language', 'grammar', 'vocabulary',
        ]
        text_lower = text.lower()
        for kw in keywords:
            if kw.lower() in text_lower:
                topics.append(kw)
        # Add conversation title as a topic if not empty
        if conversation_title and conversation_title != 'Untitled':
            topics.append(conversation_title)
        return list(dict.fromkeys(topics))  # Deduplicate while preserving order

    def _get_or_create_subject(self, name: str):
        """Get existing subject or create new one."""
        subject = self.db.query(Subject).filter(
            Subject.user_id == self.current_user.id,
            Subject.name == name
        ).first()
        if not subject:
            subject = Subject(user_id=self.current_user.id, name=name)
            self.db.add(subject)
            self.db.commit()
            self.db.refresh(subject)
        return subject

    def _get_or_create_topic(self, subject_id: str, name: str):
        """Get existing topic or create new one."""
        topic = self.db.query(Topic).filter(
            Topic.subject_id == subject_id,
            Topic.name == name
        ).first()
        if not topic:
            topic = Topic(subject_id=subject_id, name=name)
            self.db.add(topic)
            self.db.commit()
            self.db.refresh(topic)
        return topic
