"""ChatGPT conversation importer service.

Parses ChatGPT export ZIP/JSON files and extracts conversations, messages,
topics, and concepts for storage in the database.
"""

import json
import zipfile
import io
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User, DataSource, Conversation, Message, Subject, Topic, KnowledgeRecord, Analysis
from app.security import get_current_user


class ChatGPTImporter:
    """Import and parse ChatGPT conversation export files."""

    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def import_zip(self, file_content: bytes, source_id: str) -> Dict[str, Any]:
        """Import a ChatGPT export ZIP file."""
        conversations = []
        try:
            with zipfile.ZipFile(io.BytesIO(file_content)) as zf:
                # Find conversation JSON files in the ZIP
                json_files = [name for name in zf.namelist() if name.endswith('.json')]
                for json_file in json_files:
                    with zf.open(json_file) as f:
                        data = json.load(f)
                        conv = self._parse_conversation(data, source_id)
                        if conv:
                            conversations.append(conv)
        except zipfile.BadZipFile:
            # Try as single JSON file
            data = json.loads(file_content.decode('utf-8'))
            conv = self._parse_conversation(data, source_id)
            if conv:
                conversations.append(conv)

        # Save to database
        imported_count = 0
        for conv_data in conversations:
            # Check for duplicate (by external_id)
            existing = self.db.query(Conversation).filter(
                Conversation.external_id == conv_data['external_id'],
                Conversation.user_id == self.current_user.id
            ).first()
            if existing:
                continue

            conversation = Conversation(
                user_id=self.current_user.id,
                source_id=source_id,
                external_id=conv_data['external_id'],
                title=conv_data.get('title'),
            )
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)

            # Save messages
            for msg in conv_data.get('messages', []):
                message = Message(
                    conversation_id=conversation.id,
                    role=msg.get('role', 'user'),
                    content=msg.get('content', ''),
                )
                self.db.add(message)

            imported_count += 1

        # Update source import count
        source = self.db.query(DataSource).filter(DataSource.id == source_id).first()
        if source:
            source.imported_count = (source.imported_count or 0) + imported_count
            source.last_sync = datetime.utcnow()
            self.db.commit()

        self.db.commit()
        return {
            "imported_count": imported_count,
            "total_found": len(conversations),
            "conversations": [{"id": c.id, "title": c.title} for c in conversations],
        }

    def _parse_conversation(self, data: Dict[str, Any], source_id: str) -> Optional[Dict[str, Any]]:
        """Parse a single conversation from ChatGPT export format."""
        try:
            # ChatGPT export format varies; handle common structures
            if isinstance(data, list):
                # Array of conversations
                results = []
                for item in data:
                    parsed = self._parse_single_conversation(item, source_id)
                    if parsed:
                        results.append(parsed)
                return results[0] if results else None  # Return first for single import
            return self._parse_single_conversation(data, source_id)
        except Exception:
            return None

    def _parse_single_conversation(self, data: Dict[str, Any], source_id: str) -> Optional[Dict[str, Any]]:
        """Parse a single conversation object."""
        try:
            # Handle different ChatGPT export formats
            title = data.get('title') or data.get('conversation_title') or 'Untitled'
            external_id = data.get('id') or data.get('conversation_id') or str(uuid.uuid4())

            messages = []
            # Handle messages array
            if 'messages' in data:
                for msg in data['messages']:
                    messages.append({
                        'role': msg.get('role', 'user'),
                        'content': msg.get('content', ''),
                    })
            elif 'mapping' in data:
                # OpenAI's newer export format uses mapping
                for key, node in data['mapping'].items():
                    if node and 'message' in node and node['message']:
                        msg = node['message']
                        messages.append({
                            'role': msg.get('author', {}).get('role', 'user'),
                            'content': msg.get('content', {}).get('parts', [''])[0] if isinstance(msg.get('content'), dict) else str(msg.get('content', '')),
                        })

            return {
                'external_id': external_id,
                'title': title,
                'messages': messages,
            }
        except Exception:
            return None

    def extract_topics_from_conversations(self, conversation_ids: List[str]) -> Dict[str, Any]:
        """Extract topics from imported conversations using simple keyword analysis."""
        # This is a lightweight extraction; full AI analysis uses OpenAI
        from app.services.ai.topic_extractor import TopicExtractor
        extractor = TopicExtractor(self.db, self.current_user)
        return extractor.extract_from_conversations(conversation_ids)
