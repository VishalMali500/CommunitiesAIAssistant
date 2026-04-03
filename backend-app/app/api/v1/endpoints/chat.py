from fastapi import APIRouter, Depends
from app.dependency.auth_dependency import get_active_user
from app.schemas.chat_schemas import UserQuery
router = APIRouter()



@router.get("/newchat")
def newchat(user = Depends(get_active_user)):
    pass

@router.post("/chat")
async def chat(query : UserQuery , user = Depends(get_active_user)):
    pass