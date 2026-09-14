from fastapi import APIRouter, Request, Response, status
from app.core.config import Settings, get_settings
from app.core.limiter import limiter
from fastapi import Depends

router = APIRouter(prefix="/health", tags=["health"], responses={404: {"description": "Not found"}})

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
)
@limiter.limit("1/minute")
async def health_check(request: Request, response: Response, settings: Settings = Depends(get_settings)):
    return {"App Name": settings.APP_NAME, "environment": settings.ENVIRONMENT}
