from fastapi import APIRouter, Depends, HTTPException
from app.schemas.application.api_db_schema import CreateUser, DbUser, LoginUser
from app.dependency.auth_dependency import get_user_role, get_db, verify_user_and_password
from sqlalchemy.orm import Session
from app.utils.utility_functions import get_hashed_password, create_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.utils.utility_functions import check_hashed_similarity
from app.dependency.auth_dependency import get_active_user
from app.services.chat_service import chatService


router= APIRouter()
bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

@router.post("/createaccount")
async def createAccount(user : CreateUser, role : str = Depends(get_user_role), db : Session = Depends(get_db)):
    if db.query(DbUser).filter(DbUser.id == user.id).first() :
        raise HTTPException(status_code=400, detail="Email already registered")
    
    print(f"---------------{len(user.password.encode('utf-8'))}")
    dbuser = DbUser(name = user.name, id = user.id, hashed_password = get_hashed_password(user.password), role = role)
    db.add(dbuser)
    db.commit()
    db.refresh(dbuser)


@router.post("/token")
async def createAccount(form_data : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    dbuser = db.query(DbUser).filter(DbUser.id == form_data.username).first()
    if dbuser is None :
        raise HTTPException(status_code=404, detail="Unauthorised User")
    if check_hashed_similarity(form_data.password, dbuser.hashed_password) == False:
        raise HTTPException(status_code=404, detail="Invalid Password")
    token = create_token(dbuser.id, dbuser.role, dbuser.name)
    return {"access_token" : token, "token_type": "bearer"}

@router.post("/chat")
async def chat(query : str , user = Depends(get_active_user)):
    return await chatService(query)




