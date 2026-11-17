from pydantic import BaseModel
from fastapi import APIRouter, Response, HTTPException
from sqlmodel import select

from ..models import User
from ..database import SessionDep 
from ..security import verify_password, create_token, DUMMY_HASH
from ..config import COOKIE_EXPIRE_TIME

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginData(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(max_length=128)

@router.post("/login")
def login(data: LoginData, response: Response, session: SessionDep):
    user = session.exec(select(User).where(User.username == data.username)).first()

    hashed = user.password_hash if user else DUMMY_HASH
    valid = verify_password(data.password, hashed)

    if not user or not valid:
        raise HTTPException(401, "Usuário ou senha inválidos")

    response.set_cookie(
        "access_token", 
        create_token(user.username), 
        httponly=True, 
        secure=True, 
        samesite="strict", 
        max_age=COOKIE_EXPIRE_TIME
    )
    return {"ok": True}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token", httponly=True, secure=True, samesite="strict")
    return {"message": "Usuario delogado com sucesso!"}

    

    
