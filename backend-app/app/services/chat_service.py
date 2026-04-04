import uuid
from sqlalchemy.orm import Session
from app.schemas.application.api_db_schema import chatLists
from app.utils.utility_functions import getchatlist
from langchain.messages import HumanMessage, AIMessage

async def chatService(query: str, user: str, threadid : uuid.UUID, db: Session, embeddings_model, vdb):
    chatlist = getchatlist(threadid, user, db)
    annotated_messages = [ HumanMessage(content= m.get("content")) if m.get("role")== "human"  else AIMessage(content= m.get("content")) for m in chatlist ] 
    annotated_messages.extend(HumanMessage(content=query))
    
    