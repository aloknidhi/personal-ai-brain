"""AI Study Planner - generates structured study plans."""

from sqlalchemy.orm import Session
from app.models.user import User, StudyPlan, Task, Topic, KnowledgeRecord
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class StudyPlanner:
    """Generate personalized study plans based on user goals and knowledge."""

    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def generate_plan(
        self,
        title: str,
        goal: str,
        topics: List[str],
        daily_hours: int,
        days: int,
        start_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Generate a structured study plan."""
        if not start_date:
            start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=days)

        # Create the study plan
        plan = StudyPlan(
            user_id=self.current_user.id,
            title=title,
            start_date=start_date,
            end_date=end_date,
        )
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)

        # Distribute topics across days
        tasks_per_day = max(1, len(topics) // days) if topics else 1
        task_count = 0

        for day in range(days):
            day_start = start_date + timedelta(days=day)
            day_end = day_start + timedelta(hours=daily_hours)

            # Select topics for this day
            day_topics = topics[task_count:task_count + tasks_per_day] if topics else []
            for topic_name in day_topics:
                topic = self.db.query(Topic).filter(Topic.name == topic_name).first()
                task = Task(
                    plan_id=plan.id,
                    topic_id=topic.id if topic else None,
                    title=f"Study: {topic_name}",
                    status="upcoming",
                    deadline=day_end,
                )
                self.db.add(task)
                task_count += 1

        self.db.commit()
        return {
            "plan_id": plan.id,
            "title": plan.title,
            "start_date": plan.start_date.isoformat() if plan.start_date else None,
            "end_date": plan.end_date.isoformat() if plan.end_date else None,
            "total_tasks": len(plan.tasks) if plan.tasks else 0,
            "daily_hours": daily_hours,
            "duration_days": days,
        }
