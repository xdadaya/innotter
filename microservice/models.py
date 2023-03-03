from uuid import UUID

from pydantic import BaseModel


class PageStatistics(BaseModel):
    owner_id: UUID
    page_id: UUID
    posts_amount: int
    followers_amount: int
    likes_amount: int
