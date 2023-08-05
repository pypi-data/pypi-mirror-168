from typing import Optional

from pydantic import BaseModel  # pylint:disable=no-name-in-module


class TaskCreate(BaseModel):
    name: str
    time: str
    active: bool
    is_one_time: bool
    notify: bool
    weekdays: str


class Task(TaskCreate):
    id: str


class TaskUpdate(BaseModel):
    name: Optional[str]
    time: Optional[str]
    active: Optional[bool]
    is_one_time: Optional[bool]
    notify: Optional[bool]
    weekdays: Optional[str]
