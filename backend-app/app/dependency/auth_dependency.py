from app.core.get_user_role import getrole
from app.schemas.application.api_db_schema import CreateUser, LoginUser, DbUser
from fastapi import HTTPException
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from fastapi import Depends
from app.utils.utility_functions import check_hashed_similarity


engine = create_engine("postgresql://postgres:vishal@localhost:5432/UserDatabase")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



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
        
