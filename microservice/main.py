from fastapi import FastAPI, Request, HTTPException
from microservice.models import PageStatistics
from microservice.token_verify import TokenVerify
from microservice.page_statistics_service import PageStatisticsService
from uuid import UUID


app = FastAPI()


@app.get('/page-statistics/{page_id}')
async def index(page_id: UUID, request: Request) -> PageStatistics:
    try:
        token = request.headers["Authorization"]
        user_id = TokenVerify.token_verify(token)
    except KeyError:
        raise HTTPException(status_code=403, detail="No authorization")
    try:
        page_statistics = PageStatisticsService.get(str(page_id).replace("-", ""))
    except KeyError:
        raise HTTPException(status_code=404, detail="Not found")
    if page_statistics["owner_id"] == user_id:
        return page_statistics
    else:
        raise HTTPException(status_code=403, detail="You are not an owner of this page")
