from pydantic import BaseModel
from datetime import datetime


class ArticleCreate(BaseModel):
    title: str
    content: str
    is_published: bool = False


class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_published: bool | None = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True
