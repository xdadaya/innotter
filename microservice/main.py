from fastapi import FastAPI, Request, HTTPException
from microservice.models import PageStatistics
from microservice.token_verify import TokenVerify
from microservice.page_statistics_service import PageStatisticsService
from uuid import UUID
from typing import Any


app = FastAPI()


@app.get('/page-statistics/{page_id}', response_model=PageStatistics)
async def index(page_id: UUID, request: Request) -> Any:
    try:
        token = request.headers["Authorization"]
        user_id = TokenVerify.token_verify(token)
    except KeyError:
        raise HTTPException(status_code=403, detail="No authorization")
    return PageStatisticsService.get(str(page_id).replace("-", ""), user_id)
