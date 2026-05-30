import datetime
import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from models.state import TaskState


class Task(BaseModel):
    task_id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier for the task")
    name: str = Field(description="Name of the task")
    state: TaskState = Field(default=TaskState.PENDING, description="Current state of the task")
    due_date: Optional[datetime.datetime] = Field(default=None, description="Due date and time of the task (YYYY-MM-DD-hh-mm)")

    def __str__(self):
        return f"Task(id={self.task_id}, name='{self.name}', state={self.state}, due_date={self.due_date})"

    def __repr__(self):
        return f"Task(task_id={self.task_id}, name='{self.name}', state={self.state}, due_date={self.due_date})"