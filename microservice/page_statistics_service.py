from microservice.models import PageStatistics
from microservice.db import table


class PageStatisticsService:
    @staticmethod
    def get(page_id: str) -> PageStatistics:
        return table.get_item(Key={"page_id": page_id})["Item"]
