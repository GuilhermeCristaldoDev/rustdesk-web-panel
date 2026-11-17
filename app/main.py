from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from .database import create_db_and_tables
from .routers import clients, auth
from .dependencies import current_user, optional_user

STATIC_DIR = Path(__file__).resolve().parent / "static"
PAGES_DIR = Path(__file__).resolve().parent / "pages"

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(clients.router, dependencies=[Depends(current_user)])    

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def login_page(user: str | None = Depends(optional_user)):
    if user:
        return RedirectResponse("/panel", status_code=303)
    return FileResponse(PAGES_DIR / "login.html")
    
@app.get("/panel")
def panel_page(user: str | None = Depends(optional_user)):
    if not user:
        return RedirectResponse("/") 
    return FileResponse(PAGES_DIR / "panel.html")

