from fastapi import APIRouter, Depends, HTTPException
from app.schemas.application.api_db_schema import CreateUser, DbUser
from app.dependency.auth_dependency import get_user_role, get_db
from sqlalchemy.orm import Session
from app.utils.utility_functions import get_hashed_password

router= APIRouter()


@router.post("/createaccount")
async def createAccount(user : CreateUser, role : str = Depends(get_user_role), db : Session = Depends(get_db)):
    if db.query(DbUser).filter(DbUser.id == user.id).first() :
        raise HTTPException(status_code=400, detail="Email already registered")
    
    print(f"---------------{len(user.password.encode('utf-8'))}")
    dbuser = DbUser(name = user.name, id = user.id, hashed_password = get_hashed_password(user.password), role = role)
    db.add(dbuser)
    db.commit()
    db.refresh(dbuser)
    

