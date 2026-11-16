from pathlib import Path 
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

connect_args = {"check_same_thread": False}
engine = create_engine(f"sqlite:///{DATA_DIR / 'database.db'}", connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
