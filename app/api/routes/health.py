from fastapi import APIRouter, status
from app.core.config import Settings, get_settings
from fastapi import Depends

router = APIRouter(prefix="/health", tags=["health"], responses={404: {"description": "Not found"}})

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
)
async def health_check(settings: Settings = Depends(get_settings)):
    return {"environment": settings.ENVIRONMENT}
