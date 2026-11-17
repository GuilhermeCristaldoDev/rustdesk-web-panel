import jwt
from pwdlib import PasswordHash
from datetime import datetime, timezone, timedelta

from .config import JWT_SECRET, TOKEN_HOURS, ALGORITHM

_ph = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _ph.verify(plain_password, hashed_password)

def create_token(username: str) -> str:
    expire_token = datetime.now(timezone.utc) + timedelta(hours=TOKEN_HOURS)
    return jwt.encode({"sub": username, "exp": expire_token}, JWT_SECRET, algorithm=ALGORITHM)

def decode_token(token: str) -> str:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    return payload["sub"]


DUMMY_HASH = hash_password("qualquer-coisa")