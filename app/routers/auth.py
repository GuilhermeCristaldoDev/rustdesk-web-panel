from pydantic import BaseModel
from fastapi import APIRouter, Response, HTTPException
from sqlmodel import select

from ..models import User
from ..database import SessionDep 
from ..security import verify_password, create_token
from ..config import COOKIE_EXPIRE_TIME

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginData(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginData, response: Response, session: SessionDep):
    user = session.exec(select(User).where(User.username == data.username)).first()

    if not user or not verify_password(data.password, user.password_hash):
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
    response.delete_cookie(key="access_token")
    return {"message": "Usuario delogado com sucesso!"}

    

    
