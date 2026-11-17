
import jwt
from .security import decode_token
from fastapi import Cookie, HTTPException


def current_user(access_token: str | None = Cookie(default=None)) -> str:
    if not access_token:
        raise HTTPException(status_code=401, detail="Sessão inválida")

    try:
        username = decode_token(access_token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    else:
        return username

def optional_user(access_token: str | None = Cookie(default=None)) -> str | None:
    if not access_token:
        return None

    try:
        username = decode_token(access_token)
    except jwt.PyJWTError:
        return None
    else:
        return username