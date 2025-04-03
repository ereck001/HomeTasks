from pydantic import BaseModel


class ItemRaw(BaseModel):
    name: str


class ItemBase(ItemRaw):
    done_at: str | None


class TaskBase(BaseModel):
    name: str
    description: str
    done_at: str | None


class Item(ItemBase):
    item_id: int = 0
    is_done: bool


class Task(TaskBase):
    item_id: int = 0
    is_done: bool
