from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import create_db_and_tables
from .routers import clients, auth


STATIC_DIR = Path(__file__).resolve().parent / "static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(clients.router)    
app.include_router(auth.router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_page():
    return FileResponse(f"{STATIC_DIR / 'index.html'}")



