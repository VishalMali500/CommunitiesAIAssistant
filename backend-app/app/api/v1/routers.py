from fastapi import APIRouter
from app.api.v1.endpoints import authentication, chat
router = APIRouter(prefix="/api/v1")

router.include_router(authentication.router)
router.include_router(chat.router)