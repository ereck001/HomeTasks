from pydantic import BaseModel


class Item(BaseModel):
    item_id: int = 0
    name: str
    is_done: bool
    done_at: str


class Task(BaseModel):
    item_id: int = 0
    name: str
    description: str
    is_done: bool
    done_at: str
