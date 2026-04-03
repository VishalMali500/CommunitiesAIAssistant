from fastapi import APIRouter
from app.api.v1.endpoints import authentication
router = APIRouter(prefix="/api/v1")

router.include_router(authentication.router)