from pydantic import BaseModel


class ItemRaw(BaseModel):
    name: str


class TaskRaw(BaseModel):
    name: str
    description: str


class ItemBase(ItemRaw):
    done_at: str | None


class TaskBase(TaskRaw):
    done_at: str | None


class Item(ItemBase):
    item_id: int = 0
    is_done: bool


class Task(TaskBase):
    item_id: int = 0
    is_done: bool


class UserBase(BaseModel):
    name: str
    password: str


class User(UserBase):
    id: int = 0
    name: str
    password: str
    role: int
