from fastapi import APIRouter, Depends
from app.dependency.auth_dependency import get_active_user

router = APIRouter()




@router.post("/chat")
async def chat(query : str , user = Depends(get_active_user)):
    return {"user": user , "query" : query }