from typing import Optional

from pydantic import BaseModel


class PageStatistics(BaseModel):
    owner_id: str
    page_id: str
    posts_amount: Optional[int] = None
    followers_amount: Optional[int] = None
    likes_amount: Optional[int] = None
