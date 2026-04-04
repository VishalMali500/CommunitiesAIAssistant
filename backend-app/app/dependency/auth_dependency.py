from app.core.get_user_role import getrole
from app.schemas.application.api_db_schema import CreateUser, LoginUser, DbUser
from fastapi import HTTPException, Request
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from fastapi import Depends
from app.utils.utility_functions import check_hashed_similarity
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.config import Settings

engine = create_engine("postgresql://postgres:vishal@localhost:5432/UserDatabase")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
bearer  = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
set_obj = Settings()


def get_user_role(user : CreateUser):
    roledata = getrole()
    role = roledata.roles_db.get(user.id)
    if role is None:
        raise HTTPException(status_code= 404, detail="User is not allowed to use this application" )
    return role

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_registered_user(user : LoginUser, db : Session = Depends(get_db)):
    if db.query(DbUser).filter(DbUser.id == user.id).first() is None :
        raise HTTPException(status_code=404, detail = "User is not registered" )
    return True



def verify_user_and_password(user : LoginUser, db : Session = Depends(get_db), valid_user : bool = Depends(is_registered_user)):
    if check_hashed_similarity (user.password, db.query(DbUser).filter(DbUser.id == user.id).first().hashed_password) == False:
        raise HTTPException(detail="Incorrect Password", status_code=404)
    return True
        
def get_active_user(token : str = Depends(bearer), db : Session = Depends(get_db) ):
    token_data = jwt.decode(token, set_obj.jwt_secret_code, algorithms="HS256")
    if token_data.get("id") is None:
        raise HTTPException(status_code=404, detail="Invalid Token")
    user  = db.query(DbUser).filter(DbUser.id  == token_data.get("id") ).first().id
    if user is None :
        raise HTTPException(status_code=404, detail="user not found in database")
    return user

def get_embeddings(request : Request):
    return request.app.state.embedding_model
def get_embeddings(request : Request):
    return request.app.state.vdatabse