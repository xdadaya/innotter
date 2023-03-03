from uuid import UUID

from fastapi import FastAPI, Request, HTTPException

from microservice.models import PageStatistics
from microservice.page_statistics_service import PageStatisticsService
from microservice.token_verify import TokenVerify

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        token = request.headers.get("Authorization")
        user_id = TokenVerify.token_verify(token)
        request.state.uid = user_id
    except KeyError:
        raise HTTPException(status_code=403, detail="No authorization")
    return await call_next(request)


@app.get('/page-statistics/{page_id}', response_model=PageStatistics)
async def index(page_id: UUID, request: Request) -> PageStatistics:
    return PageStatisticsService.get(str(page_id).replace('-', ''), request.state.uid)
