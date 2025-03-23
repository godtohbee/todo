from pydantic import BaseModel


class TodoBase(BaseModel):
    user_id: str
    title: str
    description: str
    is_completed: bool


class Todo(TodoBase):
    id: str


class TodoCreate(TodoBase):
    iscompleted: bool = False
    pass

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None