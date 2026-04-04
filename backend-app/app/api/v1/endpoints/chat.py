from fastapi import APIRouter, Depends
from app.dependency.auth_dependency import get_active_user,get_db, get_embeddings,get_vector_database
from app.schemas.chat_schemas import UserQuery
from app.schemas.application.api_db_schema import newChat, chatLists,chatThreads
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.utils.utility_functions import getchatlist
from typing import List
from datetime import datetime, timezone
from app.services.chat_service import chatService

router = APIRouter()



@router.post("/chat")
def chat(payload : newChat ,user = Depends(get_active_user), db = Depends(get_db), embeddings_model = Depends(get_embeddings), vdb = Depends(get_vector_database) ):
    if payload.threadid is None:
        payload = newChat(user = payload.user, threadid= uuid.uuid4, query = payload.query)
        db.query(chatThreads).add(chatThreads(id = payload.threadid, user_id  = user, title=  "xx", updated_at= datetime.now(timezone.utc), created_at=datetime.now(timezone.utc)))
        db.commit()
        db.refresh()
    response = chatService(payload.query, user, payload.threadid, db, embeddings_model, vdb)
    return 
    
@router.get("/getchat/{threadid}")
async def chat(threadid : uuid.UUID , user: str = Depends(get_active_user), db = Depends(get_db)):
    sorted_chat_list = getchatlist(threadid, user, db)
    return sorted_chat_list