from typing import Optional

from pydantic import BaseModel  # pylint:disable=no-name-in-module


class Task(BaseModel):
    id: Optional[str]
    name: Optional[str]
    time: Optional[str]
    active: Optional[bool]
    is_one_time: bool = False
    notify: bool = False
    weekdays: str = "0123456"


class TaskUpdate(BaseModel):
    name: Optional[str]
    time: Optional[str]
    active: Optional[bool]
    is_one_time: Optional[bool]
    notify: Optional[bool]
    weekdays: Optional[str]
