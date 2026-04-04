from passlib.context import CryptContext
from app.core.config import get_settings
import jwt 
from datetime import timedelta, datetime
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.application.api_db_schema import chatThreads, chatLists
import json

pass_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_hashed_password(password : str):
    return pass_context.hash(password)

def check_hashed_similarity(plain_pass, hashed_pass):
    return pass_context.verify(plain_pass,hashed_pass )

def create_token(id: str, role: str, name:str):
    set_obj = get_settings()
    to_encode  = {"id": id, "name" : name , "role" : role, "tet":int((datetime.utcnow() + timedelta(minutes=set_obj.token_expiry_time)).timestamp()) , "tit":int(datetime.utcnow().timestamp()) }
    return jwt.encode(to_encode, set_obj.jwt_secret_code, algorithm = "HS256")

def getchatlist(threadid: UUID, user : str, db: Session):
    messages = ( db.query(chatLists).filter(chatLists.chatthread_id == threadid).order_by(chatLists.created_at).all())

    return list(map(lambda x: json.dumps(x), messages))
    