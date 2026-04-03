from app.core.get_user_role import getrole
from app.schemas.application.api_db_schema import CreateUser
from fastapi import HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

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
        
