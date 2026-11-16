import os 
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
TOKEN_HOURS = 8
COOKIE_EXPIRE_TIME = TOKEN_HOURS * 60 * 60