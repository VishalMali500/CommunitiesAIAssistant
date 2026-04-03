from fastapi import APIRouter, Depends, HTTPException
from app.schemas.application.api_db_schema import CreateUser, DbUser, LoginUser
from app.dependency.auth_dependency import get_user_role, get_db, verify_user_and_password
from sqlalchemy.orm import Session
from app.utils.utility_functions import get_hashed_password, create_token
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


@router.post("/login")
async def createAccount(user : LoginUser, _ = Depends(verify_user_and_password), db : Session = Depends(get_db)):
    dbuser = db.query(DbUser).filter(DbUser.id == user.id).first()
    token = create_token(dbuser.id, dbuser.role, dbuser.name)
    return {"access_token" : token, "token_type": "bearer"}
    

