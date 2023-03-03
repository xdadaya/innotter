from fastapi import HTTPException

from microservice.db import PageStatisticsDatabase
from microservice.models import PageStatistics


class PageStatisticsService:
    @staticmethod
    def get(page_id: str, user_id: str) -> PageStatistics:
        page = PageStatisticsDatabase.get_item(page_id)
        if page["owner_id"] != user_id:
            raise HTTPException(status_code=403, detail="Not owner")
        return page
